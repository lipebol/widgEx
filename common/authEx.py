from googleapiclient.discovery import build
from google.oauth2 import service_account
from .loadEx import load, system


class authentication:
    
    def __authorize(self, auth: str | None, scope: str | None) -> object:
        if auth and scope:
            return service_account.Credentials.from_service_account_info(
                load.jsonEx(data=system.decr(variable=auth), to_objectpy=True), 
                scopes=[system.decr(variable=scope)]
            )
        
    @staticmethod
    def service(
        *, name: str, version: str, key: str | None = None, 
        auth: str | None = None, scope: str | None = None
    ) -> object:
        return build(
            name, version, developerKey=system.decr(variable=key) if key else key, 
            credentials=authentication().__authorize(auth, scope), 
            cache_discovery=False
        )
