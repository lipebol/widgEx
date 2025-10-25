from datetime import datetime
from dbus import Interface, PROPERTIES_IFACE, SessionBus
from dotenv import load_dotenv
import json
from logging import basicConfig, info, INFO
from os import environ, getenv, path
from pathlib import Path
from pytz import timezone
from subprocess import run, PIPE
from time import sleep


class load:

    load_dotenv()

    basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=INFO, datefmt='%Y-%m-%d %H:%M:%S'
    )

    @staticmethod
    def quiet(func):
        def wrapper(*args, **kwargs):
            sleep(1)
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def path(path: str | None = None, *, join: list | str | None = None) -> Path:
        path = Path(path) if path else Path.cwd()
        if join:
            if isinstance(join, str):
                join = [join]
            return path.joinpath(*join)
        return path

    @staticmethod
    def checkpath(_path: str, *, dir: str | bool = False) -> bool:
        return path.exists(_path)

    @staticmethod
    def variable(var: str, *, load: bool = True, add: str | None = None) -> str:
        if add:
            environ[var] = add
        return getenv(var) if load else var

    @staticmethod
    def jsonEx(
        *, path: str | None = None, data: str | dict | None = None, 
        to_string: bool = False, to_objectpy: bool = False
    ):
        if not path and data:
            if to_string:
                data = json.dumps(data)
            if to_objectpy:
                data = json.loads(data)
            return data
        with open(path, 'w' if data else 'r') as _jsonEx:
            if not data:
                return json.load(_jsonEx)
            json.dump(data, _jsonEx, indent=5)

    @staticmethod
    def tmpfile(*, path: str, filename: str | None = None) -> str:
        return load.path(
            path, join='tmp.json' if not filename else f'{filename}.json'
        )

    @staticmethod
    def timezone_default(timezone: str | None = None) -> str:
        return 'America/Sao_Paulo' if not timezone else timezone

    @staticmethod
    def now(*, all: bool = True):
        if (now := datetime.now(tz=timezone(load.timezone_default()))):
            return now.strftime('%Y-%m-%d') if not all else now.isoformat()
   
    @quiet
    @staticmethod
    def info(_info: str) -> str:
        return info(_info)


class system:
    
    @staticmethod
    def dbus(
        name: str | None = None, objectpath: str | None = None, 
        interface: str | None = None, propertie: str | None = None, 
        *, projectname: str | None = None
    ) -> dict | None:
        try:
            if projectname:
                name, objectpath, interface, propertie = (
                    load.variable(f'{projectname.upper()}_DBUS_{var}')
                    for var in ['NAME','OBJECTPATH','INTERFACE','PROPERTIE']
                )
            return load.jsonEx(
                data=Interface(
                    SessionBus().get_object(name, objectpath), PROPERTIES_IFACE
                ).Get(interface, propertie), to_string=True, to_objectpy=True
            )
        except Exception as error:
            load.info(error)

    def __shell(self, command: str):
        return run(command, shell=True, stdout=PIPE, text=True).stdout.strip()

    @staticmethod
    def decr(*, variable: str | None = None, value: str | None = None):
        if (load_decr := load.variable('A7S6I002TMK6SUT5W')): # set in "/etc/environment"
            return system().__shell(load_decr % {"arg": value or f"${variable}"})
        raise Exception(load_decr)