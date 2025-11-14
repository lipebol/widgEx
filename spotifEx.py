from common.addEx import add
from common.dbEx import mongodb
from common.httpEx import httpEx
from common.loadEx import load, system
from common.mountEx import mount
from time import sleep

class init:

    @add.exception
    @staticmethod
    def metadata(name: str) -> dict:
        if (dbus := system.dbus(projectname=name)):
            return dict((key.split(':')[1], value) for key, value in dbus.items())

    @add.exception
    @staticmethod
    def trackid(trackid: str | None) -> str | None:
        if trackid and 'ad' not in trackid and (
            track := mongodb.select((collection := '_trackid'), _id=True)[0]
        ).get('id') != trackid:
            return mongodb.update(
                collection, filter={'_id': track.get('_id')}, 
                update={'id': trackid}
            )

    @add.exception
    @staticmethod
    def trackfind(trackid: str) -> str | list | None:
        if (
            track := mongodb.select(
                'tracks', filter={'trackid': trackid}, fields={'_id': 1}
            )
        ):
            if (
                daylist := mongodb.select(
                    'daylists', filter={
                        'date': load.now(all=False),
                        'track': (track := track[0].get('_id'))
                    }, fields={'listen': 1}
                )
            ):
                return daylist
            return track

    @add.exception
    @staticmethod
    def genrefind(genre: dict, collection='genres') -> str:
        if genre and isinstance(genre, dict):
            return genre[0].get('_id') if (
                genre := mongodb.select(
                    collection, filter=(genre_data := genre), 
                    fields={'_id': 1}
                )
            ) else mongodb.insert(collection, data=genre_data)


    @add.exception
    @staticmethod
    def artistfind(artist: str, collection='artists'):
        if (_artist := mongodb.select(
                collection, filter={
                    'name': (artist := ''.join(artist))
                }, fields={'_id': 1}
            )
        ):
            return _artist[0].get('_id')
        if (
            _scrape := httpEx.scrape(
                url=(everynoise := load.variable('EVERYNOISE')) + 
                'lookup.cgi', params={'who': artist}
            )
        ):
            _artist = mount.data(name=artist)
            for idx, i in enumerate(_scrape):
                _url = everynoise + _scrape[idx]['href']
                if 'â' in i.text:
                    _artist['profile'] = _url
                else:
                    _artist['genres'].append(
                        init.genrefind(
                            mount.data(name=i.text, url=_url)
                        )
                    )
            return mongodb.insert(collection, data=_artist)
        return 'Not Found.'

    @add.exception
    @staticmethod
    def daylist(track: str | list, collection='daylists') -> str | dict:
        if isinstance(track, list):
            return mongodb.update(
                collection, filter={
                    '_id': (track := track[0]).get('_id')
                }, update={'listen': track.get('listen')+1}
            )
        return mongodb.insert(
            collection, data=mount.data(
                track=track, date=load.now(all=False)
            )
        )

    @add.exception
    @staticmethod
    def spotifEx(metadata: dict):
        del metadata['albumArtist']
        metadata['artist'] = init.artistfind(metadata.get('artist'))
        return init.daylist(mongodb.insert('tracks', data=metadata))

    @add.exception        
    @staticmethod
    def run(widgEx: str):
        if mongodb.setconfig(widgEx):
            load.info(f'{widgEx}...')
            if (
                metadata := init.metadata(widgEx)
            ) and init.trackid(
                trackid := metadata.get('trackid')
            ):
                if (track := init.trackfind(trackid)):
                    return load.info(init.daylist(track))
                return load.info(init.spotifEx(metadata))

if __name__ == '__main__':
    try:
        while True:
            init.run('spotifEx')
            sleep(5)
    except KeyboardInterrupt:
        load.info('Exit.')
    except Exception as error:
        system.notifysend(message=error)