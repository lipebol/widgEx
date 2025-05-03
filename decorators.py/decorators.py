

class Decorators:

    dev = None
    
    def __init__(self):
        self.name = "World"

    @staticmethod
    def exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                return f"🚨 {error} (👉 @{str(func).split(' ')[1]} 👈)"
        return wrapper

    @exceptions
    def text(self, name=None) -> str:
        return f"Hello {self.dev if self.dev else self.name if not name else name}!"

    @classmethod
    def textcustom(cls, name=None) -> str:
        cls.dev = 'Bro' if not name else name
        return f"{cls().text()}✌️"

    @exceptions
    @staticmethod
    def sum(a: int, b: int) -> str:
        return f"{a} + {b} é {int(a+b)}"


print(Decorators().text())
print(Decorators.textcustom())
print(Decorators.sum(2,'3'))


