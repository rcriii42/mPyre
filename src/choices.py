"""choices - replacement for random.choices function for python<3.6"""

import random
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect


def choices(population, weights=None, *, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.
    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.

    from: https://github.com/python/cpython/blob/master/Lib/random.py
    """
    n = len(population)
    if cum_weights is None:
        if weights is None:
            _int = int
            n += 0.0  # convert to float for a small speed improvement
            return [population[_int(random.random() * n)] for i in _repeat(None, k)]
        cum_weights = list(_accumulate(weights))
    elif weights is not None:
        raise TypeError('Cannot specify both weights and cumulative weights')
    if len(cum_weights) != n:
        raise ValueError('The number of weights does not match the population')
    total = cum_weights[-1] + 0.0  # convert to float
    if total <= 0.0:
        raise ValueError('Total of weights must be greater than zero')
    bisect = _bisect
    hi = n - 1
    return [population[bisect(cum_weights, random.random() * total, 0, hi)]
            for i in _repeat(None, k)]
