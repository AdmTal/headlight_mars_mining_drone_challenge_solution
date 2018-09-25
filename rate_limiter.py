import time
import threading


def rate_limit_to_x_calls_per_second(calls_per_second):
    """
    Decorator to limit function calls to max of X per second
    """
    lock = threading.Lock()

    if calls_per_second > 0:
        max_wait_time_between_calls = 1.0 / float(calls_per_second)

    def decorate(func):
        last_call_time = [0.0]

        def rate_limited_function(args, *kargs):
            if not calls_per_second:
                return func(args, *kargs)
            lock.acquire()
            elapsed = time.clock() - last_call_time[0]
            wait_time_remaining = max_wait_time_between_calls - elapsed

            if wait_time_remaining > 0:
                time.sleep(wait_time_remaining)

            lock.release()

            ret = func(args, *kargs)
            last_call_time[0] = time.clock()
            return ret

        return rate_limited_function

    return decorate
