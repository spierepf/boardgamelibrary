import functools

from busypie import wait


def wait_at_most(duration, unit):
    def decorator_wait_at_most(func):
        @functools.wraps(func)
        def wrapper_wait_at_most(*args, **kwargs):
            def wrapper():
                try:
                    func(*args, **kwargs)
                    return True
                except:
                    return False

            wait().at_most(duration, unit).until(wrapper)

        return wrapper_wait_at_most

    return decorator_wait_at_most
