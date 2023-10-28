import typing


def need_authorization(function: typing.Callable):
    def wrapper(*args):
        print(f"[+]Calling {function.__name__}")
        return function(*args)

    return wrapper


@need_authorization
def soma(a, b):
    print(a + b)
    return a + b


print(soma(2, 3))
