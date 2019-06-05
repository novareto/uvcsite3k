import errno
import os
import signal


class Timeout(Exception):
    pass


def timeout(seconds=10, err_type=Timeout, err_msg=os.strerror(errno.ETIME)):
    """Timeout wrapper
    """

    def decorator(func):

        def _handle_timeout(signum, frame):
            raise err_type(err_msg)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator
