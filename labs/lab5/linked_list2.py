"""Lab 5: Linked List Exercises

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

All of the code from lecture is here, as well as some exercises to work on.
"""
from __future__ import annotations
from typing import Any, List, Optional


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self, item: list) -> None:
        """Initialize a new empty linked list containing the given items.
        The first node in the linked list contains the first item in <items>.
        """
        if len(item) == 0:
            self._first = None
        else:
            self._first = _Node(item[0])
            curr = self._first
            for i in range(1, len(item)):
                curr.next = _Node(item[i])
                curr = curr.next










    # ------------------------------------------------------------------------
    # Methods from lecture/readings
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        result = []
        curr = self._first
        while curr is not None:
            result.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(result) + ']'


    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        """
        curr = self._first
        curr_index = 0
        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1
        if curr is None:
            raise IndexError
        else:
            return curr.item


    def insert(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert(100, 2)
        Traceback (most recent call last):
        IndexError
        """
        node = _Node(item)
        if index == 0:
            self._first, node.next = node, self._first
        else:
            node = _Node(item)
            curr = self._first
            curr_index = 0
            while curr.next is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1
            if curr.next is None and curr_index < index - 1:
                raise IndexError
            elif curr.next is None and curr_index == index - 1:
                # insert
                curr.next, node.next = node, curr.next
            elif curr.next is not None and curr_index == index - 1:
                # insert
                curr.next, node.next = node, curr.next



    # ------------------------------------------------------------------------
    # Lab Task 1
    # ------------------------------------------------------------------------
    # TODO: implement this method
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        count = 0
        curr = self._first
        while curr is not None:
            curr = curr.next
            count += 1
        return count



    # TODO: implement this method
    def count(self, item: Any) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        count = 0
        curr = self._first
        while curr is not None:
            if curr.item == item:
                count += 1
            curr = curr.next
        return count

    # TODO: implement this method
    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """
        index = 0
        curr = self._first
        while curr is not None:
            if curr.item == item:
                break
            curr = curr.next
            index += 1
        if curr is None:
            raise ValueError
        else:
            return index




    # TODO: implement this method
    def __setitem__(self, index: int, item: Any) -> None:
        """Store item at position <index> in this list.

        Raise IndexError if index >= len(self).

        >>> lst = LinkedList([1, 2, 3])
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        >>> lst[3] = 300
        Traceback (most recent call last):
        IndexError
        """
        curr_index = 0
        curr = self._first
        change = 0
        while curr is not None:
            if curr_index == index:
                curr.item = item
                change += 1
                break
            curr = curr.next
            curr_index += 1
        if change == 0:
            raise IndexError

    def remove(self, item: Any) -> None:
        """
        Remove the first occurance of the item in list
        Mutate the list
        >>> lst = LinkedList([1, 2, 1])
        >>> lst.remove(1)
        >>> str(lst)
        '[2 -> 1]'
        >>> lst = LinkedList([1, 2, 1])
        >>> lst.remove(2)
        >>> str(lst)
        '[1 -> 1]'
        >>> lst = LinkedList([1])
        >>> lst.remove(1)
        >>> str(lst)
        '[]'
        >>> lst1 = LinkedList([2, 1, 3])
        >>> lst1.remove(3)
        >>> str(lst1)
        '[2 -> 1]'
        >>> lst2 = LinkedList([2])
        >>> lst2.remove(1)
        Traceback (most recent call last):
        ValueError
        """

        if self._first is None:
            raise ValueError
        elif self._first.item == item:
            self._first = self._first.next
        else:
            prev = self._first
            while prev.next is not None:
                if prev.next.item == item:
                    prev.next = prev.next.next
                    return
                prev = prev.next
            if prev.next is None:
                raise ValueError


    def remove_first_double(self):
        """
        It is 2016 March tt2. Remove second of two adjacent nodes with duplicate values.
        >>> lst = LinkedList([3, 2, 2, 3, 3])
        >>> lst.remove_first_double()
        >>> str(lst)
        '[3 -> 2 -> 3 -> 3]'
        """
        prev = None
        curr = self._first
        while curr is not None:
            if prev is None:
                pass
            else:
                if prev.item == curr.item:
                    prev.next = curr.next
                    return
            prev = curr
            curr = curr.next

    def concat(self, other: LinkedList) -> None:
        """
        Concatenates other self and sets other to contain no values. (that is, other
        should have its .first attribute None)
        Raise exception if other starts empty
        >>> lst = LinkedList([1, 2, 3])
        >>> lst2 = LinkedList([1, 2, 3])
        >>> lst.concat(lst2)
        >>> str(lst)
        '[1 -> 2 -> 3 -> 1 -> 2 -> 3]'
        >>> str(lst2)
        '[]'
        """
        if self._first is None:
            self._first = other._first
            other._first = None
        else:
            curr = self._first
            while curr.next is not None:
                curr = curr.next
            curr.next = other._first
            other._first = None



    def remove_max(self):
        """
        raise an empty Error if linked list is already empty
        >>> lst = LinkedList([10, 20, 50, 40, 30])
        >>> lst.remove_max()
        50
        >>> str(lst)
        '[10 -> 20 -> 40 -> 30]'
        >>> lst = LinkedList([1])
        >>> lst.remove_max()
        1
        >>> str(lst)
        '[]'
        >>> lst = LinkedList([2, 2])
        >>> lst.remove_max()
        2
        >>> str(lst)
        '[2]'
        """
        max = 0
        mprev = None
        mcurr = self._first
        curr = self._first
        if self._first is None:
            return
        while curr.next is not None:
            if curr.next.item > max:
                max = curr.next.item
                mprev = curr
                mcurr = curr.next
            curr = curr.next
        if mcurr == self._first:
            max = self._first.item
            self._first = None
        else:
            mprev.next = mprev.next.next
        return max


    def remove_max2(self):
        """
        raise an empty Error if linked list is already empty
        >>> lst = LinkedList([10, 20, 50, 40, 30])
        >>> lst.remove_max()
        50
        >>> str(lst)
        '[10 -> 20 -> 40 -> 30]'
        >>> lst = LinkedList([1])
        >>> lst.remove_max()
        1
        >>> str(lst)
        '[]'
        >>> lst = LinkedList([2, 2])
        >>> lst.remove_max()
        2
        >>> str(lst)
        '[2]'
        """
        big = 0
        curr = self._first
        while curr is not None:
            if curr.item > big:
                big = curr.item
            curr = curr.next
        prev = self._first
        if self._first is None:
            raise EmptyError
        elif self._first.item == big:
            self._first = self._first.next
        else:
            while prev.next is not None:
                if prev.next == big:
                    prev.next = prev.next.next
                    return
                prev = prev.next



    def insert2(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert2(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert2(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert2(100, 2)
        Traceback (most recent call last):
        IndexError
        """


    def pop_at_index(self, index):
        """
        Pop item at index, if index < 0 or index >= length LinkedList, raise Error
        >>> lst = LinkedList([1, 2, 3, 4])
        >>> lst.pop_at_index(0)
        >>> str(lst)
        '[2 -> 3 -> 4]'
        >>> lst.pop_at_index(2)
        >>> str(lst)
        '[2 -> 3]'
        >>> lst.pop_at_index(2)
        Traceback (most recent call last):
        IndexError
        """
        if self._first is None:
            raise EmptyError
        if index == 0:
            self._first = self._first.next
        curr = self._first
        curr_index = 0
        while curr.next is not None and curr_index < index - 1:
            curr = curr.next
            curr_index += 1
        if curr.next is None and curr_index == index - 1:
            raise IndexError
        if curr.next is None and curr_index < index - 1:
            raise IndexError
        if curr.next is not None and curr_index == index - 1:
            curr.next = curr.next.next




    def remove_first_satisfier(self, predicate):
        """
        Remove first node whose value satisfies predicate. If there is no
        such node, leave self as is.
        >>> lst = LinkedList([1, 2, 3, 4])
        >>> def f(n): return n >= 3
        >>> lst.remove_first_satisfier(f)
        >>> str(lst)
        '[1 -> 2 -> 4]'
        >>> lst.remove_first_satisfier(f)
        >>> str(lst)
        '[1 -> 2]'
        """
        curr = self._first
        if self._first is None:
            raise EmptyError
        elif predicate(self._first.item):
            self._first = self._first.next
        else:
            while curr.next is not None:
                if predicate(curr.next.item):
                    curr.next = curr.next.next
                    return
                curr = curr.next



def swap(lst: LinkedList, i: int, j:int) -> None:
    """
    Swap the values stored at indexes <i> and <j> in the given linked list

    Precondition: i and j are >= 0.

    Raise an IndexError if i or j (or both) are too large (Out of bounds of the list)
    >>> linky = LinkedList([10, 20, 30, 40, 50])
    >>> swap(linky, 0, 3)
    >>> str(linky)
    '[40 -> 20 -> 30 -> 10 -> 50]'
    >>> swap(linky, 1, 5)
    Traceback (most recent call last):
    IndexError
    >>> swap(linky, 5, 0)
    Traceback (most recent call last):
    IndexError
    """
    k = 0
    curr = lst._first
    while curr is not None:
        k += 1
        curr = curr.next
    if j > k - 1 or i > k - 1:
        raise IndexError
    else:
        jcurr = None
        icurr = None
        curr = lst._first
        t = 0
        while curr is not None:
            if t == j:
                jcurr = curr
            if t == i:
                icurr = curr
            t += 1
            curr = curr.next
        jcurr.item, icurr.item = icurr.item, jcurr.item







class EmptyError(Exception):
    pass



if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all()
    import doctest
    doctest.testmod()
