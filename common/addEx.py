from .notifEx import notific
from traceback import format_exc


class add:

    @staticmethod
    def exception(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                return notific.add_event(
                    summary=type(error).__name__, description=format_exc(), colorId='11'
                )
        return wrapper

    