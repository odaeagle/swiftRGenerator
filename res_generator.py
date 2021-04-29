def foo(x):
    """
    >>> foo(2)
    3
    """
    return x + 1

def test_something():
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import sys
    import pytest
    pytest.main(['res_generator.py'])
