from common.addEx import add
from common.dbEx import mongodb
from common.httpEx import httpEx
from common.loadEx import load, system
from common.mountEx import mount
from common.notifEx import notific
from time import sleep

class init:

    mongodb.setdb('spotifEx')

    @add.exception
    @staticmethod
    def env():
        if not load.checkpath(tmpfile := load.tmpfile(path='/tmp')):
            load.jsonEx(path=tmpfile, data=mongodb.select('_envs')[0])
        for key, value in load.jsonEx(path=tmpfile).items():
            yield load.variable(key, add=value)

    @add.exception
    @staticmethod
    def metadata() -> dict:
        if (dbus := system.dbus(projectname='spotifEx')):
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
    def trackfind(trackid: str) -> dict | None:
        if (track := mongodb.select(
                'tracks', filter={
                    'date': load.now(all=False),
                    'about.trackid': trackid
                }, fields={'listen': 1}
            )
        ):
            return track[0]

    @add.exception
    @staticmethod
    def uplisten(track: dict) -> str:
        return mongodb.update(
            'tracks', filter={'_id': track.get('_id')}, 
            update={'listen': track.get('listen')+1}
        )

    @add.exception
    @staticmethod
    def genrefind(genre: dict):
        if genre and isinstance(genre, dict):
            return genre[0].get('_id') if (
                genre := mongodb.select(
                    'genres', filter=(genre_data := genre), 
                    fields={'_id': 1}
                )
            ) else mongodb.insert('genres', data=genre_data)


    @add.exception
    @staticmethod
    def artistfind(artist: str):
        if (_artist := mongodb.select(
                'artists', filter={'name': (artist := ''.join(artist))},
                fields={'_id': 1}
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
            return mongodb.insert('artists', data=_artist)

    @add.exception
    @staticmethod
    def spotifEx(metadata: dict):
        del metadata['albumArtist']
        return mongodb.insert(
            'tracks', data=mount.data(
                about={
                    **metadata, 
                    'artist': init.artistfind(metadata.get('artist'))
                }
            )
        )

    @add.exception        
    @staticmethod
    def run():
        load.info('spotifEx...')
        if list(init.env()):
            if (
                metadata := init.metadata()
            ) and init.trackid(
                trackid := metadata.get('trackid')
            ):
                if (track := init.trackfind(trackid)):
                    return init.uplisten(track)
                return init.spotifEx(metadata)

if __name__ == '__main__':
    try:
        while True:
            init.run()
            sleep(5)
    except KeyboardInterrupt:
        load.info('Exit.')
    except Exception as error:
        system.notifysend(message=error)

    