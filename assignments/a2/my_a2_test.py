import datetime
import pytest
import os

from typing import List, Dict
from tm_trees import FileSystemTree
from tm_trees import TMTree

def test_task3():
    path = 'example-directory'
    file_tree = FileSystemTree(path)
    file_tree.update_rectangles((0, 0, 800, 600))
    file_tree.get_tree_at_position((376, 168))
    file_tree.get_tree_at_position((377, 168))

def test_task4():
    path = 'example-directory'
    file_tree = FileSystemTree(path)
    file_tree.update_rectangles((0, 0, 800, 600))
    q = file_tree._subtrees[0]._subtrees[0]._subtrees[0]._subtrees[0]
    assert q._name == 'Q2.pdf'
    q.change_size(0.01)
    assert q._parent_tree.data_size == 70
    assert q._parent_tree._parent_tree.data_size == 72
    assert q._parent_tree._parent_tree._parent_tree.datasize == 152

def test_task4_update_data_size():
    path = 'example-directory'
    file_tree = FileSystemTree(path)
    file_tree.update_rectangles((0, 0, 800, 600))
    draft = file_tree._subtrees[0]._subtrees[1]
    draft.data_size = 61
    assert file_tree.update_data_sizes() == 154

