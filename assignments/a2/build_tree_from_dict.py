import csv
from typing import List, Dict
from tm_trees import TMTree


import random  # For Task 2
from typing import Any, Optional, List, Tuple

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


def _rough(str1: str, dic: Dict) -> None:
    """Mutate a dictionary by one paper's Category"""
    split1 = str1.split(':')
    for i in range(len(split1)):
        if i == len(split1) - 1:
            if split1[i] in dic:
                pass
            else:
                dic[split1[i]] = []
        elif split1[i] in dic:
            dic[split1[i]].append(split1[i + 1])
        else:
            dic[split1[i]] = [split1[i + 1]]
    for item in dic:
        if not isinstance(dic[item], tuple):
            dic[item] = list(set(dic[item]))


def _raw_leave(str1: str, split: list, dic: Dict) -> None:
    """
    Mutate a dictionary by one paper's name. Str1 represents the last catagory
    which is the parent of paper_name, Set dic[paper_name] to a tuple contains
    author, doi, citations
    """
    paper_name = split[1]
    dic[str1].append(paper_name)
    dic[paper_name] = (split[0], split[-2], split[-1].strip())


def _indexing(lst: list, max_len: int) -> List[tuple]:
    """
    Return a list contains tuples. The first item of tuple is
    starting index and second item is ending index and the third item
    is a bool. If bool is true, then needs to combine string, otherwise
    dont do anything
    >>> lst = [0, 3, 7, 9]
    >>> _indexing(lst, 13)
    [(0, 4, True), (4, 7, False), (7, 10, True), (10, 13, False)]
    >>> lst = [4, 5, 6, 7]
    >>> _indexing(lst, 13)
    [(0, 5, False), (4, 6, True), (6, 6, False), (6, 8, True), (8, 13, False)]
    >>> lst = [4, 5, 6, 12]
    >>> _indexing(lst, 13)
    [(0, 5, False), (4, 6, True), (6, 6, False), (6, 13, True), (13, 13, False)]
    """
    new_lst = []
    # does includes endpoint
    if lst[0] != 0:
        new_lst.append((0, lst[0]+1, False))
    for i in range(len(lst)):
        # quote_pair[i] exists and i % 2,
        # then quote_pair[i+1] must exists
        if i % 2 == 0:
            tup = (lst[i], lst[i+1] + 1, True)
            new_lst.append(tup)
        # quote_pair[i] exists and i % 2
        # then quote_pair[i+1] may or may not exists
        elif i % 2 != 0:
            if i < len(lst) - 1:
                tup = (lst[i] + 1, lst[i+1], False)
                new_lst.append(tup)
            elif i == len(lst) - 1:
                tup = (lst[i] + 1, max_len, False)
                new_lst.append(tup)
    return new_lst

def _spliting(str1) -> list:
    """
    Given a string of the format from data.csv, split it by ',' and
    allowed ',' inside each category
    >>> file = open(DATA_FILE, 'r')
    >>> a = file.readlines()
    >>> k = a[1]
    >>> _spliting(k)
    ['"Fisher, P. and Hankley, W. and Wallentine, V."', 'Separation of Introductory Programming and Language Instruction', '1973', 'FLP: other: language agnostic approaches', 'http://doi.acm.org/10.1145/800010.808066', '6\\n']
    >>> _spliting(a[46])
    ['"Luker, P. A."', '"Never Mind the Language, What About the Paradigm?"', '1989', 'FLP: specific paradigms', 'http://doi.acm.org/10.1145/65293.71442', '8\\n']
    """
    split = str1.split(',')
    quote_pair = []
    for i in range(len(split)):
        if split[i][0] == '"':
            if split[i][-1] != '"':
                quote_pair.append(i)
        elif split[i][-1] == '"':
            quote_pair.append(i)
        else:
            pass
    assert len(quote_pair) % 2 == 0
    if len(quote_pair) == 0:
        return split
    new_lst = []
    partition = _indexing(quote_pair, len(split))
    for tup in partition:
        start, end, boolen = tup
        # means needs to combine
        if boolen:
            str_comb = ''
            for i in range(start, end):
                str_comb += split[i] + ','
            str_comb = str_comb[0:-1]
            new_lst.append(str_comb)
        # means no need to combine
        else:
            for i in range(start, end):
                new_lst.append(split[i])
    assert len(new_lst) <= len(split)
    return new_lst


def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """

    # TODO: Implement this helper, or remove it if you do not plan to use it

    file = open(DATA_FILE, 'r')
    a = file.readlines()
    dic = {}
    # use to store CS1's subtrees
    dic['CS1'] = []
    for i in range(1, len(a)):
        my_split = _spliting(a[i])
        # update cs1 subtree
        dic['CS1'].append((my_split[3].split(':'))[0])
        _rough(my_split[3], dic)
        last_catogry = (my_split[3].split(':'))[-1]
        _raw_leave(last_catogry, my_split, dic)
    file.close()
    return dic

class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    def __init__(self, root: Optional[Any], subtrees: list) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also do len(subtree) here
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> 1 in t  # Same as t.__contains__(1)
        True
        >>> 5 in t
        True
        >>> 4 in t
        False
        """
        if self.is_empty():
            return False

        # item may in root, or subtrees
        if self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if item in subtree:
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + str(self._root) + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                s += subtree._str_indented(depth + 1)
            return s


def build_tree_from_dict(dic, root: str):
    if type(dic[root]) == tuple:
        a = Tree(root, [dic[root]])
        return a
    else:
        subtrees = dic[root]
        lst = []
        for subtree in subtrees:
            lst.append(build_tree_from_dict(dic, subtree))
        k = Tree(root, lst)
        return k

