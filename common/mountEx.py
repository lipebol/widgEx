from .loadEx import load
from dataclasses import asdict, dataclass, field
from inspect import getmembers, isclass, signature
from sys import modules

@dataclass
class Genre:
    name: str
    url: str

@dataclass
class Artist:
    name: str
    profile: str = field(default='')
    genres: list = field(default_factory=list)

@dataclass
class Track:
    about: dict
    date: str = field(default=load.now(all=False))
    listen: int = field(default=1)

@dataclass
class Event_Date:
    dateTime: str = field(default=load.now())
    timeZone: str = field(default=load.timezone_default())

@dataclass
class Event:
    summary: str
    description: str
    colorId: str
    start: dict
    end: dict 
    visibility: str = field(default="public")


class mount:

    @property
    def __classes(self):
        for classname in [
            classname for classname, classdesc in getmembers(
                modules[__name__], isclass
            ) if load.path(__file__).name.strip('.py') in str(classdesc) 
            and classname != self.__class__.__name__
        ]:
            if (params := signature(globals()[classname].__init__).parameters):
                yield {
                    classname: [
                        key for key, value in params.items() 
                        if '=' not in str(value) and key != 'self'
                    ]
                }

    @staticmethod
    def data(*, classname: str | None = None, **kwargs):
        if not classname:
            for classEx in mount().__classes:
                if list(classEx.values())[0] == list(kwargs.keys()):
                    classname = ''.join(classEx.keys())
                    break
        return asdict(globals()[classname](**kwargs))
        
        
