from .authEx import authentication
from .loadEx import load, system
from .mountEx import mount


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


    