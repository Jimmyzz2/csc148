"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will write two different functions that operate on a Stack.
Pay attention to whether or not the stack should be modified.
"""
from typing import Any, List


###############################################################################
# Task 1: Practice with stacks
###############################################################################
class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in a last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in this stack. The end of the list represents
    #     the top of the stack.
    _items: List

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return self._items == []

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        Raise an EmptyStackError if this stack is empty.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        if self.is_empty():
            raise EmptyStackError
        else:
            return self._items.pop()


class EmptyStackError(Exception):
    """Exception raised when an error occurs."""
    pass


def size(s: Stack) -> int:
    """Return the number of items in s.

    >>> s = Stack()
    >>> size(s)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size(s)
    3
    """
    side_stack = Stack()
    count = 0
    # Pop everything off <s> and onto <side_stack>, counting as we go.
    while not s.is_empty():
        side_stack.push(s.pop())
        count += 1
    # Now pop everything off <side_stack> and back onto <s>.
    while not side_stack.is_empty():
        s.push(side_stack.pop())
    # <s> is restored to its state at the start of the function call.
    # We consider that it was not mutated.
    return count


# TODO: implement this function!
def remove_big(s: Stack) -> None:
    """Remove the items in <stack> that are greater than 5.

    Do not change the relative order of the other items.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> s.push(8)
    >>> s.push(4)
    >>> remove_big(s)
    >>> s.pop()
    4
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    """
    helper_stack = Stack()
    while not s.is_empty():
        item = s.pop()
        if (type(item) == float or type(item) == int) and item > 5:
            pass
        else:
            helper_stack.push(item)
    while not helper_stack.is_empty():
        item = helper_stack.pop()
        s.push(item)



# TODO: implement this function!
def double_stack(s: Stack) -> Stack:
    """Return a new stack that contains two copies of every item in <stack>.

    We'll leave it up to you to decide what order to put the copies into in
    the new stack.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> new_stack = double_stack(s)
    >>> s.pop()  # s should be unchanged.
    29
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    >>> new_items = []
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> sorted(new_items)
    [1, 1, 29, 29]
    """
    helper_stack = Stack()
    new_stack = Stack()
    while not s.is_empty():
        item = s.pop()
        helper_stack.push(item)
    while not helper_stack.is_empty():
        item = helper_stack.pop()
        new_stack.push(item)
        new_stack.push(item)
        s.push(item)
    return new_stack


def is_balance(msg):
    """
    >>> is_balance('[()]')
    True
    >>> is_balance('{[())]}')
    False
    """
    if len(msg) == 0:
        return True
    s = Stack()
    s.push(msg[0])
    index = 0
    while index <= len(msg) - 2:
        first = s.pop()
        index += 1
        second = msg[index]
        if (first == '[' and second == ']') or (first == '(' and second == ')') or (first == '{' and second == '}'):
            pass
        else:
            s.push(first)
            s.push(second)
    if s.is_empty():
        return True
    else:
        return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()