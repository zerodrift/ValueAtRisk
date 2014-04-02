import functools
import weakref

class Memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.

    >>> counter = 0
    >>> @Memoized
    ... def count():
    ...     global counter
    ...     counter += 1
    ...     return counter

    >>> counter = 0
    >>> Memoized.reset()
    >>> count()
    1
    >>> count()
    1
    >>> Memoized.reset()
    >>> count()
    2

    >>> class test(object):
    ...     @Memoized
    ...     def func(self):
    ...         global counter
    ...         counter += 1
    ...         return counter
    >>> testobject = test()
    >>> counter = 0
    >>> testobject.func()
    1
    >>> testobject.func()
    1
    >>> Memoized.reset()
    >>> testobject.func()
    2
    """

    caches = weakref.WeakSet()

    def __init__(self, func):
        self.func = func
        self.cache = {}
        Memoized.caches.add(self)

    def __call__(self, *args):
      try:
          return self.cache[args]
      except KeyError:
          value = self.func(*args)
          self.cache[args] = value
          return value
      except TypeError:
          # uncachable -- for instance, passing a list as an argument.
          # Better to not cache than to blow up entirely.
          return self.func(*args)

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)

    @staticmethod
    def reset():
        for memo in Memoized.caches:
            memo.cache = {}

if __name__ == '__main__':
    import doctest
    doctest.testmod()