from .loadEx import load, system
from .httpEx import httpEx
from googleapiclient.discovery import build
from google.oauth2 import service_account

class auth:
    
    def __google(self, _auth: str | None, _scope: str | None) -> object:
        return service_account.Credentials.from_service_account_info(
            load.jsonEx(data=system.decr(variable=_auth), to_objectpy=True), 
            scopes=[system.decr(variable=_scope)]
        )
    
    @staticmethod
    def googleservice(
        *, name: str, version: str, _auth: str | None = None, 
        _scope: str | None = None, _authkey: str | None = None,
    ) -> object:
        if _auth and _scope:
            _auth = auth().__google(_auth, _scope)
        elif _authkey:
            _authkey = system.decr(variable=_authkey)
        return build(
            name, version, developerKey=_authkey, credentials=_auth, 
            cache_discovery=False
        )

    @staticmethod
    def __spotify(trackid: str):
        if (data := load.jsonEx(data=load.variable('SPOTIFYAPI'), to_objectpy=True)):
            if not (token := data.get('token')) or (
                load.date(load.now())-load.date(data.get('created_at'))
            ).total_seconds() >= 3600:
                if (
                    token := system.encr(
                        value = httpEx.fetch(
                            url = data.get('get_token'), data = {
                                **(params := data.get('params')), 
                                "client_id": system.decr(value=params.get('client_id')),
                                "client_secret": system.decr(value=params.get('client_secret'))
                            }
                        ).get('access_token')
                    )
                ):
                    if (alldata := load.jsonEx(path=(tmpfile := load.tmpfile(path='/tmp')))):
                        alldata['SPOTIFYAPI'] = load.jsonEx(
                            data={**data, "token": token, "created_at": load.now()}, 
                            to_string=True
                        )
                        load.jsonEx(path=tmpfile, data=alldata)
                        load.envs()
            return token, data.get('get_data') % {'id': trackid.split('/')[-1]}

    @staticmethod
    def spotify(func):
        def wrapper(trackid: str):
            token, get_data = auth.__spotify(trackid)
            if token and (
                    metadata := httpEx.fetch(
                        headers={'Content-Type': 'application/json', 'AuthExternal': token},
                        data=load.jsonEx(data={'query': get_data}, to_string=True),
                        url="http://localhost/api/v2/graphql/"   
                    ).get('data').get('spotifyAPI')
                ):
                    if (get_data := metadata.get('data')):
                        metadata = get_data[0]
                    return func(metadata)
            raise Exception('There was probably an error while generating the token.')
        return wrapper