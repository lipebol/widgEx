from bson.objectid import ObjectId
from common.authEx import auth
from common.dbEx import mongodb
from common.loadEx import load, system
from common.mountEx import mount
from common.notifEx import notific
import pyarrow as arrow

class init:
 
    @staticmethod
    def metadata(widgEx: str) -> dict:
        if (dbus := system.dbus(service=widgEx)):
            return dict((key.split(':')[1], value) for key, value in dbus.items()) 

    @staticmethod
    def genres(genre: dict, collection='genres') -> str:
        if isinstance(genre, dict):
            return find[0].get('_id') if (
                find := mongodb.select(
                    collection, filter=genre, fields={'_id': 1}
                )
            ) else mongodb.insert(collection, data=genre)

    @staticmethod
    def artists(artists: list) -> object:
        for artist in artists:
            if (id := artist.get('id')):
                yield ObjectId(id)
            elif (genres := artist.get('genres')):
                artist['genres'] = list(map(init.genres, genres))
                yield mongodb.insert('artists', data=artist)

    @staticmethod
    def markets(available_markets: list) -> object:
        ISO_3166_1 = mongodb.select('ISO_3166-1', database='common', _id=True)
        for join_type in ['right outer','left anti']:
            yield ISO_3166_1.join(
                arrow.Table.from_arrays(
                    [arrow.array(available_markets)], names=['code']
                ), keys='code', join_type=join_type
            ).select([0]).drop_null().to_pydict().get('_id')
    
    @staticmethod
    def album(album: dict) -> object:
        if (id := album.get('id')):
            return ObjectId(id)
        elif (markets := album.get('available_markets')):
            album['available_markets'], album['no_available_markets'] = tuple(
                init.markets(album.get('available_markets'))
            )
            return mongodb.insert('albums', data=album)

    @staticmethod
    def daylist(track: str | dict, collection='daylists') -> str | dict:
        if isinstance(track, dict):
            if (track := track.get('id')):
                if (
                    find := mongodb.select(
                        collection, filter=(
                            daylistfilter := {
                                'date': load.now(all=False), 'track': track
                            }
                        ), fields={'listen': 1, '_id': 0}
                    )
                ):
                    return mongodb.update(
                        collection, filter=daylistfilter, 
                        update={'listen': find[0].get('listen')+1}
                    )
        return mongodb.insert(
            collection, data=mount.data(track=track, date=load.now(all=False))
        )

    @auth.spotify
    @staticmethod
    def spotifEx(track: dict):
        if not (error := track.get('error')):
            if not track.get('id'):
                track['artists'] = list(init.artists(track.get('artists')))
                track['album'] = init.album(track.get('album'))
                track = str(mongodb.insert('tracks', data=track))
            return init.daylist(track)
        load.info(error)

    @notific.exception
    @staticmethod
    def run(trackid: str):
        if (metadata := init.metadata(widgEx)):
            if (newtrackid := metadata.get('trackid')) != trackid:
                if '/com/spotify/ad/' not in newtrackid:
                    load.info(init.spotifEx(newtrackid))
                    return newtrackid
            return trackid
        return 'Offline'

if __name__ == '__main__':
    try:
        if (trackid := mongodb.setconfig((widgEx := load.widgex()))):
            while (trackid := init.run(trackid)):
                load.info(f'{widgEx} ({trackid})')
    except KeyboardInterrupt:
        load.info('Exit.')
    except Exception as error:
        system.notifysend(message=error)