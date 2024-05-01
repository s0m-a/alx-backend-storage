#!/usr/bin/env python3

from typing import Callable, Optional, Union
from functools import wraps
import redis
from uuid import uuid4

'''
    This section focuses on the process of writing strings to Redis.
'''


def count_calls(method: Callable) -> Callable:
    '''
    This decorator keeps track of the number of times a method is called.
    '''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            This is a wrapper function.
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and
    outputs for a specific function.
    """
    key = method.__qualname__
    input = key + ":input"
    output = key + ":output"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Decorator wrapper functionality """
        self._redis.rpush(input, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(output, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    This function replays the execution history of a given function.
    Parameters:
        - method: The function to be decorated.
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    call = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, call))
    input = cache.lrange(name + ":input", 0, -1)
    output = cache.lrange(name + ":output", 0, -1)
    for x, y in zip(input, output):
        print("{}(*{}) -> {}".format(name, x.decode('utf-8'),
                                     y.decode('utf-8')))


class Cache:
    '''
        Created cache class.
    '''
    def __init__(self):
        '''
            Initializing the cache
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
            Store data in the cache by utilizing store()
        '''
        randKey = str(uuid4())
        self._redis.set(randKey, data)
        return randKey

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''
             retrieve an data from the cache by utilizing get()
        '''
        value = self._redis.get(key)
        if fn:
            val = fn(value)
        return val

    def get_str(self, key: str) -> str:
        '''
             retrieve an str from the cache by utilizing the get_str
        '''
        val = self._redis.get(key)
        return val.decode('utf-8')

    def get_int(self, key: str) -> int:
        '''
             Retrieve an integer from the cache by utilizing the get_int method
        '''
        val = self._redis.get(key)
        try:
            val = int(value.decode('utf-8'))
        except Exception:
            val = 0
        return val
