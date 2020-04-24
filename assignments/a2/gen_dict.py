from typing import List
DATA_FILE = 'cs1_papers.csv'
def _rough(str1: str, str2: str, str3: str, str4: str, dic: dict):
    """
    Given four strings, mutate a dictionary to add regisiter paht like a:b:c:d
    into the dictionary. If the path already exits do nothing, else, regisiter
    children corresbondingly
    """
    dict = {}
    split1 = str1.split(':')
    for i in range(len(split1)):
        if i == len(split1) - 1:
            if split1[i] in dict:
                pass
            else:
                dict[split1[i]] = []
        elif split1[i] in dict:
            dict[split1[i]].append(split1[i + 1])
        else:
            dict[split1[i]] = [split1[i + 1]]
    split1 = str2.split(':')
    for i in range(len(split1)):
        if i == len(split1) - 1:
            if split1[i] in dict:
                pass
            else:
                dict[split1[i]] = []
        elif split1[i] in dict:
            dict[split1[i]].append(split1[i + 1])
        else:
            dict[split1[i]] = [split1[i + 1]]
    split1 = str3.split(':')
    for i in range(len(split1)):
        if i == len(split1) - 1:
            if split1[i] in dict:
                pass
            else:
                dict[split1[i]] = []
        elif split1[i] in dict:
            dict[split1[i]].append(split1[i + 1])
        else:
            dict[split1[i]] = [split1[i + 1]]
    split1 = str4.split(':')
    for i in range(len(split1)):
        if i == len(split1) - 1:
            if split1[i] in dict:
                pass
            else:
                dict[split1[i]] = []
        elif split1[i] in dict:
            dict[split1[i]].append(split1[i + 1])
        else:
            dict[split1[i]] = [split1[i + 1]]
    for item in dict:
        dict[item] = list(set(dict[item]))

    return dict


def spliting(str1) -> list:
    """
    Given a string of the format from data.csv, split it by ',' and
    allowed ',' inside each category
    >>> file = open(DATA_FILE, 'r')
    >>> a = file.readlines()
    >>> k = a[1]
    >>> spliting(k)
    ['"Fisher, P. and Hankley, W. and Wallentine, V."', 'Separation of Introductory Programming and Language Instruction', '1973', 'FLP: other: language agnostic approaches', 'http://doi.acm.org/10.1145/800010.808066', '6\\n']
    >>> spliting(a[46])
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
    partition = indexing(quote_pair, len(split))
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





def indexing(lst: list, max_len: int) -> List[tuple]:
    """
    Return a list contains tuples. The first item of tuple is
    starting index and second item is ending index and the third item
    is a bool. If bool is true, then needs to combine string, otherwise
    dont do anything
    >>> lst = [0, 3, 7, 9]
    >>> indexing(lst, 13)
    [(0, 4, True), (4, 7, False), (7, 10, True), (10, 13, False)]
    >>> lst = [4, 5, 6, 7]
    >>> indexing(lst, 13)
    [(0, 5, False), (4, 6, True), (6, 6, False), (6, 8, True), (8, 13, False)]
    >>> lst = [4, 5, 6, 12]
    >>> indexing(lst, 13)
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














    # # combine
    # assert len(quote_pair) >= 2
    # new_split = []
    # index = 0
    # for i in range(quote_pair[0]):
    #     new_split.append(split[i])
    #     index += 1
    # for i in range(len(quote_pair)):
    #     if i % 2 == 0:
    #         # quote_pair[i] exists and i % 2,
    #         # then quote_pair[i+1] must exists
    #         str_comb = ''
    #         while index <= quote_pair[i+1]:
    #             str_comb += split[quote_pair[index]]
    #             index += 1
    #         new_split.append(str_comb)
    #     elif i % 2 != 0:
    #         # quote_pair[i] exists and i % 2
    #         # then quote_pair[i+1] may or may not exists
    #         if i == len(quote_pair) - 1:
    #         # case quote_pair[i + 1] does not exits
    #             pass
    #         elif i < len(quote_pair) - 1:
    #         # case quote_pair[i + 1] does exits
    #             while index < quote_pair[i+1]:
    #                 single_str = split[quote_pair[index]]
    #                 new_split.append(single_str)
    #                 index += 1
    #     if index < len(split) - 1:
    #         while index < len(split) - 1:
    #             index += 1
    #             single_str = split[quote_pair[index]]
    #             new_split.append(single_str)
    #         return new_split
    #     else:
    #         return new_split

def test_spliting():
    """passed dammn it"""
    file = open(DATA_FILE, 'r')
    a = file.readlines()
    for i in range(len(a)):
        assert len(spliting(a[i])) == 6


def shit(l: list, d: dict) -> None:
    if l == []:
        return
    elif l[0] not in d:
        d[l[0]] = {}
        slice = l[1:]
        shit(slice, d[l[0]])
    else:
        slice = l[1:]
        shit(slice, d[l[0]])





if __name__ == '__main__':
    str1 = 'A: B: C'
    str2 = 'A: G: F'
    str3 = 'N: M'
    str4 = 'A: B: C: D'
    _rough(str1, str2, str3, str4)
    file = open(DATA_FILE, 'r')
    a = file.readlines()
    k = a[1]
    spliting(k)

