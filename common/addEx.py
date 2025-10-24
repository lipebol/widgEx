from .loadEx import load
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
                return notific.add_event(
                    summary=f"{load.path(
                        getmodule(currentframe().f_back).__file__
                    ).name.strip('.py')} ({type(error).__name__})", 
                    description=format_exc(), colorId='11'
                )
        return wrapper

    