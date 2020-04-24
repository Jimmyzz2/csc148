"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from typing import List, Tuple, Optional
from random import randint


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        # change made Task 5
        self._expanded = False
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        self._colour = r, g, b
        if subtrees == []:
            self.data_size = data_size
        else:
            self.data_size = 0
            for tmtree in self._subtrees:
                self.data_size += tmtree.data_size
        for tmtree in self._subtrees:
            tmtree._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect

        # base case
        if self.is_empty():
            return None
        elif self._subtrees == []:
            self.rect = rect
            return None
        # case vertical partition
        self.rect = rect
        x, y, width, height = rect
        if width > height:
            x_kept = x
            for i in range(len(self._subtrees) - 1):
                if self.data_size != 0:
                    partiton = self._subtrees[i].data_size / self.data_size
                else:
                    partiton = 0
                new_rect = x_kept, y, math.floor(width * partiton), height
                # change x to new x_kept
                x_kept += math.floor(width * partiton)
                # recursive call on each subtree of subtree[i]
                self._subtrees[i].update_rectangles(new_rect)
            # last rectangle has leftover width/height
            last_subtree = self._subtrees[len(self._subtrees) - 1]
            new_rect = x_kept, y, x + width - x_kept, height
            # recursive call on subtree of last subtree
            last_subtree.update_rectangles(new_rect)
            return None
        # case horizontal partition
        else:
            self.rect = rect
            y_kept = y
            for i in range(len(self._subtrees) - 1):
                if self.data_size != 0:
                    partiton = self._subtrees[i].data_size / self.data_size
                else:
                    partiton = 0
                new_rect = x, y_kept, width, math.floor(height * partiton)
                # change y to new y_kept
                y_kept += math.floor(height * partiton)
                # recursive call on each subtree of subtree[i]
                self._subtrees[i].update_rectangles(new_rect)
            # last rectangle has leftover width/height
            last_subtree = self._subtrees[len(self._subtrees) - 1]
            new_rect = x, y_kept, width, y + height - y_kept
            # recursive call on subtree of last subtree
            last_subtree.update_rectangles(new_rect)
            return None

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.is_empty() or self.data_size == 0:
            return []
        # base case displayed-tree's leave
        elif not self._expanded or self._subtrees == []:
            rect_color = self.rect, self._colour
            return [rect_color]
        # recursive case
        else:
            lst = []
            for subtree in self._subtrees:
                lst.extend(subtree.get_rectangles())
            return lst

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        if self.is_empty():
            return None
        x_in, y_in = pos
        x, y, width, height = self.rect
        # base case outside of this tree's rectangles
        # base case displayed-tree's leave
        if x + width < x_in or x_in < x or y + height < y_in or y_in < y:
            return None
        # there exists rectangles contain this point
        elif not self._expanded or self._subtrees == []:
            return self
        lst = []
        for subtrees in self._subtrees:
            x, y, width, height = subtrees.rect
            if x + width >= x_in >= x \
                    and y + height >= y_in >= y:
                lst.append((subtrees.get_tree_at_position(pos)))
        assert None not in lst
        assert len(lst) >= 1
        if len(lst) == 1:
            return lst[0]
        # choose a rectangle that is closest to origin(edges case)
        # choose leftmost or uppermost rectangle
        lst2 = []
        for rect in lst:
            x, y, width, height = rect.rect
            assert isinstance(height, int)
            # if point on right or bottom edge
            if x_in == x + width or y_in == y + width:
                lst2.append(rect)
        if len(lst2) == 1:
            return lst2[0]
        # still tie
        # return the one who has left point closet to origin
        # if tie at lst2
        if len(lst2) != 0:
            assert len(lst2) >= 2
            dist_origin_lst = []
            for rect in lst2:
                x, y, width, height = rect.rect
                dist_origin_lst.append(x ^ 2 + y ^ 2)
            return lst2[dist_origin_lst.index(min(dist_origin_lst))]
        # if not tie at lst2
        else:
            assert len(lst2) == 0
            dist_origin_lst = []
            assert len(lst) >= 1
            for rect in lst:
                x, y, width, height = rect.rect
                dist_origin_lst.append(x ^ 2 + y ^ 2)
            return lst[dist_origin_lst.index(min(dist_origin_lst))]

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self.is_empty():
            return 0
        elif self._subtrees == []:
            return self.data_size
        else:
            size = 0
            for subtrees in self._subtrees:
                size += subtrees.update_data_sizes()
            self.data_size = size
            return size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        # if destination is empty or is a leaf
        if not destination.is_empty() and destination._subtrees != [] \
                and self._subtrees == []:
            destination._subtrees.append(self)
            # remove it from its origin parent
            self._parent_tree._subtrees.remove(self)
            # assign new parent to destination
            self._parent_tree.data_size -= self.data_size
            self._parent_tree = destination
            return None
        else:
            return None

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        # lower limits cannot go below 1, no upper limit
        # rounded before change
        if self.is_empty():
            return None
        elif self._subtrees == []:
            amount = math.ceil(abs(self.data_size * factor))
            if factor < 0:
                amount = -1 * amount
            # temp = self.data_size
            self.data_size += amount
            if self.data_size < 1:
                self.data_size = 1
            return None
        else:
            return None

    def expand(self) -> None:
        """
        Change expanded to True for this tree

        Do nothing if this tree is a leaf
        """
        # if _subtrees is empty, then _expanded is False
        if self.is_empty():
            return None
        elif self._subtrees == []:
            return None
        else:
            self._expanded = True
            return None

    def expand_all(self) -> None:
        """
        Change expanded to True for this tree and all its subtrees

        Do nothing if this tree is a leaf
        """
        if self.is_empty():
            return None
        elif self._subtrees == []:
            return None
        else:
            self._expanded = True
            for subtrees in self._subtrees:
                subtrees.expand_all()
            return None

    def collapse(self) -> None:
        """
        Change expanded to False for the parent of tree

        Do nothing if the parent is None
        """
        if self.is_empty():
            return None
        elif self._parent_tree is None:
            return None
        else:
            self._parent_tree._expanded = False
            # it is like folder if you expand assignment, expand
            # a2 you collapse assignment, a2 is also collapse
            self._parent_tree._collapse_root()
            return None

    def collapse_all(self) -> None:
        """
        Change expanded to False for the parent of tree
        and all its parent trees' subtrees
        """
        if self.is_empty():
            return None
        elif self._parent_tree is None:
            self._collapse_root()
            return None
        else:
            self._parent_tree._expanded = False
            self._parent_tree.collapse_all()
            return None

    def _collapse_root(self) -> None:
        """
        Change expanded to False for this tree and all its subtrees
        """
        if self.is_empty():
            return None
        elif self._subtrees == []:
            return None
        else:
            self._expanded = False
            for subtrees in self._subtrees:
                subtrees._collapse_root()
            return None

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        # case if path is a directory
        if os.path.isdir(path):
            files = os.listdir(path)
            lst = []
            size = 0
            for file in files:
                temp = FileSystemTree(os.path.join(path, file))
                size += temp.data_size
                lst.append(temp)
            TMTree.__init__(self, os.path.basename(path), lst, size)
        # case if path is a file
        else:
            TMTree.__init__(self, os.path.basename(path),
                            [], os.path.getsize(path))

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
