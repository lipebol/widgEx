from .loadEx import load, system
from .mountEx import mount
from googleapiclient.discovery import build
from google.oauth2 import service_account


class notific:
    
    @staticmethod
    def add_event(
        *, summary: str, description: str, colorId: str, 
        date = mount.data(classname='Event_Date')
    ):
        return authentication.service(
            name='calendar', version='v3', 
            auth=load.variable('NOTIFIC_AUTH'), 
            scope=load.variable('NOTIFIC_SCOPE')
        ).events().insert(
            calendarId=system.decr(variable=load.variable('NOTIFIC_ID')), 
            body=mount.data(
                summary=summary, description=description, 
                colorId=colorId, start=date, end=date
            )
        ).execute()


class authentication:
    
    def __authorize(self, auth: str, scope: str) -> object:
        return service_account.Credentials.from_service_account_info(
            load.jsonEx(data=system.decr(variable=auth), to_objectpy=True), 
            scopes=[system.decr(variable=scope)]
        )
        
    @staticmethod
    def service(*, name: str, version: str, auth: str, scope: str) -> object:
        return build(
            name, version, credentials=authentication().__authorize(auth, scope),
            cache_discovery=False
        )
    

    