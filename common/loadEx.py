from dbus import Interface, PROPERTIES_IFACE, SessionBus
from dotenv import load_dotenv
import json
from logging import basicConfig, info, INFO
from os import environ, getenv, path
from pathlib import Path
from time import sleep


class load:

    load_dotenv()

    basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', 
        level=INFO, datefmt='%Y-%m-%d %H:%M:%S'
    )

    @staticmethod
    def exception(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                raise Exception(f"{error} (👉 @{str(func).split(' ')[1]} 👈)")
        return wrapper

    @staticmethod
    def quiet(func):
        def wrapper(*args, **kwargs):
            sleep(1)
            return func(*args, **kwargs)
        return wrapper

    @exception
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

    @exception
    @staticmethod
    def variable(var: str, *, load: bool = True, add: str | None = None) -> str:
        if add:
            environ[var] = add
        return getenv(var) if load else var

    @exception
    @staticmethod
    def jsonEx(*, path: str | None = None, data: str | None = None):
        if not path and data:
            return json.loads(json.dumps(data))
        with open(path, 'w' if data else 'r') as _jsonEx:
            if not data:
                return json.load(_jsonEx)
            json.dump(data, _jsonEx, indent=5)

    @exception
    @staticmethod
    def tmpfile(*, path: str, filename: str | None = None) -> str:
        return load.path(
            path, join='tmp.json' if not filename else f'{filename}.json'
        )
    
    @exception
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
                ).Get(interface, propertie)
            )
        except Exception as error:
            load.info(error)
