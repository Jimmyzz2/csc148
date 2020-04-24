"""Lab 6: Recursion

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few nested list functions for you to practice recursion.
"""
from typing import Union, List


def add_n(obj: Union[int, List], n: int) -> Union[int, List]:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    # if isinstance(obj, int):
    #     ...
    # else:
    #     for sublist in obj:
    #         ... add_n(sublist) ...
    if isinstance(obj, int):
        obj += n
        return obj
    else:
        lst = []
        for sublist in obj:
            lst.append(add_n(sublist, n))
        return lst




def nested_list_equal(obj1: Union[int, List], obj2: Union[int, List]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    # HINT: You'll need to modify the basic pattern to loop over indexes,
    # so that you can iterate through both obj1 and obj2 in parallel.

    # if isinstance(obj, int):
    #     ...
    # else:
    #     for sublist in obj:
    #         ... nested_list_equal(sublist) ...
    if isinstance(obj1, int) and isinstance(obj2, int):
        return obj1 == obj2
    elif isinstance(obj1, int) or isinstance(obj2, int):
        return False
    else:
        if len(obj1) != len(obj2):
            return False
        else:
            for i in range(len(obj1)):
                if not nested_list_equal(obj1[i], obj2[i]):
                    return False
            return True




def duplicate(obj: Union[int, List]) -> Union[int, List]:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    # HINT: in the recursive case, you'll need to distinguish between
    # a <sublist> that is an int and a <sublist> that is a list
    # (put an isinstance check inside the loop).

    # if isinstance(obj, int):
    #     ...
    # else:
    #     for sublist in obj:
    #         ... duplicate(sublist) ...
    if isinstance(obj, int):
        return [obj, obj]
    else:
        lst = []
        for sublist in obj:
            if isinstance(sublist, int):
                lst.append(sublist)
                lst.append(sublist)
            else:
                lst.append(duplicate(sublist))
        return lst

def count_lists(list_):
    """
    Return the number of lists, including list_, itself, contained in list_

    >>> count_lists([])
    1
    >>> count_lists([5, [1, [2, 3], 4], 6])
    3
    """
    if not isinstance(list_, list):
        return 0
    else:
        s = 0
        for item in list_:
            s += count_lists(item)
        return s + 1

def add_one(obj) -> None:
    """
    >>> lst = 1
    >>> add_one(lst)
    >>> lst
    1
    >>> lst = [1, [2, 3], [[]]]
    >>> add_one(lst)
    >>> lst
    [2, [3, 4], [[]]]
    """
    if isinstance(obj, int):
        pass
    else:
        for i in range(len(obj)):
            if isinstance(obj[i], int):
                obj[i] += 1
            else:
                add_one(obj[i])



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
