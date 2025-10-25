from .loadEx import load, system
from .notifEx import notific
from traceback import format_exc
from inspect import currentframe, getmodule


class add:

    @staticmethod
    def exception(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                _widgExname = load.path(
                    getmodule(currentframe().f_back).__file__
                ).name.strip('.py')
                try:
                    system.notifysend(
                        title=_widgExname, message=notific.add_event(
                            summary=f"{_widgExname} ({type(error).__name__})", 
                            description=format_exc(), colorId='11'
                        ).get('kind')
                    )
                except Exception as error:
                    system.notifysend(title=_widgExname, message=format_exc())
        return wrapper

    