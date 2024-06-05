"""
This script hosts several decorators that can be used for error handeling methods.
"""

import functools
import signal
import time

from orb import log


class TimeoutError(Exception):
    ...


def timeout(seconds: int = 10, error_message: str = "Function took too long, exiting"):
    """
    Decorator that adds a timeout to a function.

    Args:
        seconds (int, optional): The maximum time in seconds allowed for the function to execute. Defaults to 10.
        error_message (str, optional): The error message to raise when the function exceeds the timeout. Defaults to "Function took too long, exiting".

    Returns:
        function: The decorated function.

    Usage:
        @timeout(seconds=10, error_message="Function took too long, exiting")
        def my_function():
            # Function code here
            # If the function exceeds the timeout, a TimeoutError will be raised

    Example:
        my_function()  # Call the decorated function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that adds a timeout to the decorated function.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the decorated function if it completes within the timeout.

            Raises:
                TimeoutError: If the decorated function exceeds the specified timeout.
            """
            def _handle_timeout(signum, frame):
                raise TimeoutError(error_message)

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator


def retry_on_failure(max_retries: int = 2):
    """
    Decorator that retries a function multiple times before giving up.

    Args:
        max_retries (int, optional): The maximum number of retries. Defaults to 2.

    Returns:
        function: The decorated function.

    Usage:
        @retry_on_failure(max_retries=2)
        def my_function():
            # Function code here
            # If an exception occurs, it will retry the function up to `max_retries` times

    Example:
        my_function()  # Call the decorated function
    """

    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            """
            Wrapper function that performs the retry logic.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the decorated function if successful, or None if retries are exhausted.

            Raises:
                Exception: If the decorated function raises an exception after all retries are exhausted.
            """
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log.debug(f"Retry {retries+1}/{max_retries+1} failed: {e}")
                    retries += 1
                    time.sleep(1)  # Delay between retries
            log.error(f"Function {func.__name__} failed after {max_retries+1} retries.")
        return wrapper_retry
    return decorator_retry
