"""Prep 11 Synthesize: Recursive Sorting Algorithms

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file includes the recursive sorting algorithms from this week's prep
readings, and two short programming exercises to extend your learning about
these algorithms in different ways.
"""
from typing import Any, List, Tuple


################################################################################
# Mergesort and Quicksort
################################################################################
def mergesort(lst: List) -> List:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of mergesort; it does not mutate the
    input list.

    >>> mergesort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Divide the list into two parts, and sort them recursively.
        mid = len(lst) // 2
        left_sorted = mergesort(lst[:mid])
        right_sorted = mergesort(lst[mid:])

        # Merge the two sorted halves. Need a helper here!
        return _merge(left_sorted, right_sorted)


def _merge(lst1: List, lst2: List) -> List:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Precondition: <lst1> and <lst2> are sorted.
    """
    index1 = 0
    index2 = 0
    merged = []
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] <= lst2[index2]:
            merged.append(lst1[index1])
            index1 += 1
        else:
            merged.append(lst2[index2])
            index2 += 1

    # Now either index1 == len(lst1) or index2 == len(lst2).
    assert index1 == len(lst1) or index2 == len(lst2)
    # The remaining elements of the other list
    # can all be added to the end of <merged>.
    # Note that at most ONE of lst1[index1:] and lst2[index2:]
    # is non-empty, but to keep the code simple, we include both.
    return merged + lst1[index1:] + lst2[index2:]


def quicksort(lst: List) -> List:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of quicksort; it does not mutate the
    input list.

    >>> quicksort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Pick pivot to be first element.
        # Could make lots of other choices here (e.g., last, random)
        pivot = lst[0]

        # Partition rest of list into two halves
        smaller, bigger = _partition(lst[1:], pivot)

        # Recurse on each partition
        smaller_sorted = quicksort(smaller)
        bigger_sorted = quicksort(bigger)

        # Return! Notice the simple combining step
        return smaller_sorted + [pivot] + bigger_sorted


def _partition(lst: List, pivot: Any) -> Tuple[List, List]:
    """Return a partition of <lst> with the chosen pivot.

    Return two lists, where the first contains the items in <lst>
    that are <= pivot, and the second is the items in <lst> that are > pivot.
    """
    smaller = []
    bigger = []

    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)

    return smaller, bigger


################################################################################
# Synthesize exercises
################################################################################
# TODO: Complete the implementation of this function!
def mergesort3(lst: List) -> List:
    """Return a sorted version of <lst> using three-way mergesort.

    Three-way mergesort is similar to mergesort, except:
        - it divides the input list into *three* lists of (almost) equal length
        - the main helper merge3 takes in *three* sorted lists, and returns
          a sorted list that contains elements from all of its inputs.

    HINT: depending on your impementation, you might need another base case
    when len(lst) == 2 to avoid an infinite recursion error.

    >>> mergesort3([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    >>> mergesort([-5, 6, 3, 2, 100, 10, -3])
    [-5, -3, 2, 3, 6, 10, 100]
    >>> mergesort3([2, 1])
    [1, 2]
    >>> mergesort3([3, 4, 3, 5, 3, 6])
    [3, 3, 3, 4, 5, 6]
    >>> mergesort3([3, 4, 3, 5, 3, 6, -1])
    [-1, 3, 3, 3, 4, 5, 6]
    >>> mergesort([2, 1])
    [1, 2]

    """
    if len(lst) < 2:
        return lst[:]
    elif len(lst) == 2:
        if lst[0] <= lst[1]:
            return lst[:]
        else:
            return lst[::-1]
    else:
        first_p = len(lst) // 3
        second_p = first_p * 2
        return merge3(mergesort(lst[0:first_p]),
                      mergesort(lst[first_p:second_p]),
                      mergesort(lst[second_p:]))




# TODO: Implement this function!
# Note that we've made it public because we'll be testing it directly.
def merge3(lst1: List, lst2: List, lst3: List) -> List:
    """Return a sorted list with the elements in the given input lists.

    Precondition: <lst1>, <lst2>, and <lst3> are all sorted.

    This *must* be implemented using the same approach as _merge; in particular,
    it should use indexes to keep track of where you are in each list.
    This will keep your implementation efficient, which we will be checking for.

    Since this involves some detailed work with indexes, we recommend splitting
    up your code into one or more helpers to divide up (and test!) each part
    separately.
    >>> merge3([3], [5], [2])
    [2, 3, 5]
    >>> merge3([-1, 2, 100], [0, 1, 3], [4, 99, 101])
    [-1, 0, 1, 2, 3, 4, 99, 100, 101]
    >>> merge3([-1, 0, 1, 2, 3, 4],\
    [-1, 0, 1, 2, 3, 4],\
    [-1, 0, 1, 2, 3, 4])
    [-1, -1, -1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    >>> merge3([], [], [])
    []
    """
    i = 0
    j = 0
    k = 0
    merged = []

    while (i < len(lst1) and j < len(lst2))\
        or (i < len(lst1) and k < len(lst3))\
        or (j < len(lst2) and k < len(lst3)):
        if i == len(lst1):
            if lst2[j] <= lst3[k]:
                merged.append(lst2[j])
                j += 1
            else:
                merged.append(lst3[k])
                k += 1
        elif j == len(lst2):
            if lst1[i] <= lst3[k]:
                merged.append(lst1[i])
                i += 1
            else:
                merged.append(lst3[k])
                k += 1
        elif k == len(lst3):
            if lst1[i] <= lst2[j]:
                merged.append(lst1[i])
                i += 1
            else:
                merged.append(lst2[j])
                j += 1
        elif lst1[i] <= lst2[j] and lst1[i] <= lst3[k]:
            merged.append(lst1[i])
            i += 1
        elif lst2[j] <= lst1[i] and lst2[j] <= lst3[k]:
            merged.append(lst2[j])
            j += 1
        else:
            merged.append(lst3[k])
            k += 1
    assert (i == len(lst1) and j == len(lst2)) \
           or (i == len(lst1) and k == len(lst3)) \
           or (j == len(lst2), k == len(lst3))
    return merged + lst1[i:] + lst2[j:] + lst3[k:]






# TODO: Implement this function
def kth_smallest(lst: List, k: int) -> Any:
    """Return the <k>-th smallest element in <lst>.

    Raise IndexError if k < 0 or k >= len(lst).
    Note: for convenience, k counts from 0, so kth_smallest(lst, 0) == min(lst).

    Precondition: <lst> does not contain duplicates.

    >>> kth_smallest([10, 20, -4, 3], 0)
    -4
    >>> kth_smallest([10, 20, -4, 3], 2)
    10
    >>> kth_smallest([7, 3, 4, 5, 8, 19, 20], 2)
    5
    >>> kth_smallest([7, 3, 4, 5, 8, 19, 20], 3)
    7
    >>> kth_smallest([7, 3, 4, 5, 8, 19, 20], 4)
    8
    """
    # You may *not* sort the list here (this is easy but not very efficient).
    # Instead, use the following approach, based on quicksort:
    #   1. partition the list based on a chosen pivot:
    #       smaller, bigger = partition(...)
    #   2. Compare len(smaller) against k, and use the result to decide which
    #      list to recurse on (if any). As in your BST prep, you should only
    #      make one recursive call into either <smaller> or <bigger>, not both!
    if k < 0 or k >= len(lst):
        raise IndexError
    elif lst == []:
        return None
    elif k == 0:
        return min(lst)
    else:
        pivot = lst[0]
        smaller = [x for x in lst if x < pivot]
        eq = [x for x in lst if x == pivot]
        greater = [x for x in lst if x > pivot]
        if k <= len(smaller) - 1:
            return kth_smallest(smaller, k)
        else:
            if k <= len(smaller) + len(eq) - 1:
                return eq[0]
            else:
                return kth_smallest(greater, k - len(smaller) - len(eq))
        # infinite loop
        # smaller_eq, greater = _partition(lst[1:], pivot)
        # smaller_eq.append(lst[0])
        # if len(smaller_eq) - 1 >= k:
        #     return kth_smallest(smaller_eq, k)
        # else:
        #     return kth_smallest(greater, k - len(smaller_eq))




if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all()
