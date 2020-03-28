def singleton():
    def singleton_decorator(func):
        return _singleton_wrapper(func)

    return singleton_decorator


def _singleton_wrapper(func):
    value = None

    def wrapper(*args, **kwargs):
        nonlocal value

        if value is None:
            value = func(*args, **kwargs)

        return value

    return wrapper
