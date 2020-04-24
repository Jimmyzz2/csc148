"""
CSC148, Winter 2019
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import time
import datetime
from typing import List, Tuple
from call import Call
from customer import Customer


class Filter:
    """ A class for filtering customer data on some criterion. A filter is
    applied to a set of calls.

    This is an abstract class. Only subclasses should be instantiated.
    """
    def __init__(self) -> None:
        pass

    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data>, which match the filter
        specified in <filter_string>.

        The <filter_string> is provided by the user through the visual prompt,
        after selecting this filter.
        The <customers> is a list of all customers from the input dataset.

         If the filter has
        no effect or the <filter_string> is invalid then return the same calls
        from the <data> input.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        - all calls included in <data> are valid calls from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """
    A class for resetting all previously applied filters, if any.
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Reset all of the applied filters. Return a List containing all the
        calls corresponding to <customers>.
        The <data> and <filter_string> arguments for this type of filter are
        ignored.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        """
        filtered_calls = []
        for c in customers:
            customer_history = c.get_history()
            # only take outgoing calls, we don't want to include calls twice
            filtered_calls.extend(customer_history[0])
        return filtered_calls

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Reset all of the filters applied so far, if any"


class CustomerFilter(Filter):
    """
    A class for selecting only the calls from a given customer.
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data> made or received by the
         customer with the id specified in <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains a valid
        customer ID.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.
        """
        # The filter string is valid if and only if it contains
        # a valid customer id
        # sanity check:
        if not filter_string.isdigit():
            return data
        # it contains a valid customer ID
        # means id in customers list
        found = 0
        for customer in customers:
            if int(filter_string) == customer.get_id():
                found += 1
        if found == 0:
            return data
        # assume already did the sanity check
        # filter string is valid if and only if it contains a valid customer ID
        # from now on any string below is valid
        call_lst = []
        for customer in customers:
            if int(filter_string) == customer.get_id():
                # need both incoming and outgoing call
                call_lst.extend(customer.get_history()[0])
                call_lst.extend(customer.get_history()[1])
        # eliminate duplicate in call_lst
        # bc you can call yourself
        call_lst = list(set(call_lst))
        # eliminate call not in data
        for call in call_lst:
            if call not in data:
                call_lst.remove(call)
        data = call_lst
        return data

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """
    A class for selecting only the calls lasting either over or under a
    specified duration.
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data> with a duration of under or
        over the time indicated in the <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains the following
        input format: either "Lxxx" or "Gxxx", indicating to filter calls less
        than xxx or greater than xxx seconds, respectively.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.
        """

        # l005 = L005
        if 1 < len(filter_string) <= 4 and \
                (filter_string[0] == 'l' or filter_string[0] == 'g'):
            filter_string = filter_string[0].upper() + filter_string[1:]
        # L4 = L004
        if 1 < len(filter_string) < 4 and \
                (filter_string[0] == 'L' or filter_string[0] == 'G'):
            if filter_string[1:].isdigit():
                add_zero = (4 - len(filter_string)) * '0'
                filter_string = filter_string[0] + add_zero + filter_string[1:]
        # sanity check
        # The filter string is valid if and only if it contains the following
        # input format: either "Lxxx" or "Gxxx",
        if len(filter_string) != 4:
            return data
        # now we are sure it has len(4) can do index
        if (filter_string[0] != 'L' and filter_string[0] != 'G')\
           or not filter_string[1:3].isdigit():
            return data
        # assume already sanity check
        # from now on any string below is valid
        # wont need to consider double count bc already double count handled in
        # data
        call_lst = []
        for call in data:
            if filter_string[0] == 'L':
                if call.duration < int(filter_string[1:]):
                    call_lst.append(call)
            elif filter_string[0] == 'G':
                if call.duration > int(filter_string[1:]):
                    call_lst.append(call)
        data = call_lst
        return data

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls based on duration; " \
               "L### returns calls less than specified length, G### for greater"


class LocationFilter(Filter):
    """
    A class for selecting only the calls that took place within a specific area
    """
    def apply(self, customers: List[Customer],
              data: List[Call],
              filter_string: str) \
            -> List[Call]:
        """ Return a list of all calls from <data>, which took place within
        a location specified by the <filter_string> (at least the source or the
        destination of the event was in the range of coordinates from the
        <filter_string>).

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains four valid
        coordinates within the map boundaries.
        These coordinates represent the location of the lower left corner
        and the upper right corner of the search location rectangle,
        as 2 pairs of longitude/latitude coordinates, each separated by
        a comma and a space:
          lowerLong, lowerLat, upperLong, upperLat
        Calls that fall exactly on the boundary of this rectangle are
        considered a match as well.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.
        """
        # check four float
        # sanity check
        # check right format
        split = filter_string.split(',')
        for item in split:
            try:
                float(item)
            except ValueError:
                return data
        # all float
        # check length
        if len(split) != 4:
            return data
        # check white space
        if split[0] != split[0].strip():
            return data
        for i in range(1, len(split)):
            if split[i] != ' ' + split[i].strip():
                return data
        #  right format
        #  check in map
        for i in range(len(split)):
            split[i] = split[i].strip()
        # now length = 4 safe to do index
        if not (-79.697878 <= float(split[0]) <= -79.196382) or \
                not (-79.697878 <= float(split[2]) <= -79.196382) or \
                not (43.576959 <= float(split[1]) <= 43.799568) or \
                not 43.576959 <= float(split[3]) <= 43.799568:
            return data
        # check order:
        if float(split[0]) > float(split[2]) or \
                float(split[1]) > float(split[3]):
            return data
        # The filter string is valid if and only if it contains four valid
        # coordinates within the map boundaries.
        # assume already sanity check
        # from now on any string below is valid
        call_lst = []
        cor_lst = filter_string.split(', ')
        for call in data:
            if ((float(cor_lst[0]) <= call.src_loc[0] <= float(cor_lst[2])) and
                    (float(cor_lst[1]) <= call.src_loc[1]
                     <= float(cor_lst[3])))\
                or ((float(cor_lst[0]) <= call.dst_loc[0] <= float(cor_lst[2]))
                    and (float(cor_lst[1]) <= call.dst_loc[1]
                         <= float(cor_lst[3]))):
                call_lst.append(call)
        data = call_lst
        return data

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls made or received in a given rectangular area. " \
               "Format: \"lowerLong, lowerLat, " \
               "upperLong, upperLat\" (e.g., -79.6, 43.6, -79.3, 43.7)"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'time', 'datetime', 'call', 'customer'
        ],
        'max-nested-blocks': 4,
        'allowed-io': ['apply', '__str__'],
        'disable': ['W0611', 'W0703'],
        'generated-members': 'pygame.*'
    })
