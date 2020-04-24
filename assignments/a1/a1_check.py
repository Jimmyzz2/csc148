import datetime
import pytest
import json

from application import create_customers, process_event_history
from typing import List, Dict
from customer import Customer
from contract import TermContract, MTMContract, PrepaidContract
from phoneline import PhoneLine
from filter import DurationFilter, CustomerFilter, ResetFilter, LocationFilter
from bill import Bill
from call import Call


def test_task1_2_simple() -> None:
    # Make sure you complete Task 1 and 2
    # Reading and Recording all calls

    customers = create_customers(test_dict_small)
    customers[0].new_month(1, 2018)
    process_event_history(test_dict_small, customers)

    # Check the CallHistory objects are populated
    history = customers[0].get_call_history('111-1111')
    assert len(history) == 1
    assert len(history[0].incoming_calls) == 1, """Should only be one history object"""
    assert len(history[0].outgoing_calls) == 1

    all_records = history[0].get_monthly_history()
    all_incomings = all_records[1]
    all_outgoings = all_records[0]
    assert len(all_incomings) == 1, """All incoming calls across all month"""
    assert len(all_outgoings) == 1, """All outgoing calls across all month"""

    # Check if a call's data is populated correctly
    x = all_incomings[0]
    assert x.duration == 50
    assert x.time.year == 2018
    assert x.time.month == 1
    assert x.time.day == 1
    assert x.src_loc == (-79.42848154284123, 43.641401675960374)
    assert x.dst_loc == (-79.52745693913239, 43.750338501653374)

    # check another phone number
    history = customers[0].get_call_history('333-3333')
    assert len(history) == 1
    assert len(history[0].incoming_calls) == 1
    assert len(history[0].outgoing_calls) == 1

    all_records = history[0].get_monthly_history()
    all_incomings = all_records[1]
    all_outgoings = all_records[0]
    assert len(all_incomings) == 2, """All incoming calls across all month"""
    assert len(all_outgoings) == 1, """All outgoing calls across all month"""


def test_task1_2_with_diff_month() -> None:
    customers = create_customers(test_dict_medium)
    customers[0].new_month(1, 2018)
    customers[1].new_month(1, 2018)
    process_event_history(test_dict_medium, customers)

    customer = customers[0]
    history = customer.get_call_history('222-2222')
    assert len(history) == 1
    assert len(history[0].incoming_calls) == 0
    assert len(history[0].outgoing_calls) == 3, """222-2222 made calls in 3 diff months"""
    all_records = history[0].get_monthly_history()
    assert len(all_records[0]) == 4
    assert len(all_records[1]) == 0

    jan_records = history[0].get_monthly_history(1, 2018)
    assert len(jan_records[0]) == 1
    assert len(jan_records[1]) == 0

    feb_records = history[0].get_monthly_history(2, 2018)
    assert len(feb_records[0]) == 2
    assert len(feb_records[1]) == 0

    mar_records = history[0].get_monthly_history(3, 2018)
    assert len(mar_records[0]) == 1
    assert len(mar_records[1]) == 0


def test_task1_2_with_all() -> None:
    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    process_event_history(input_dictionary, customers)
    history = []
    expect = [(27, 26), (13, 11), (39, 36), (18, 16), (3, 8), (42, 31), (25, 23), (16, 19), (37, 40), (27, 28), (7, 12), (19, 14), (29, 17), (27, 19), (31, 29), (4, 2), (10, 19), (15, 12), (3, 6), (10, 10), (4, 2), (3, 5), (20, 22), (22, 20), (22, 37), (30, 25), (27, 26), (16, 19), (30, 45), (19, 29), (8, 7), (44, 21), (16, 23), (37, 33), (15, 18), (28, 33), (4, 4), (30, 24), (21, 25), (28, 32), (25, 20), (13, 14), (13, 18), (25, 22), (7, 10), (21, 23), (26, 33), (11, 11), (12, 10), (21, 11)]
    for customer in customers:
        v = customer.get_history()
        history.append((len(v[0]), len(v[1])))
    for i in range(len(history)):
        assert history[i] == expect[i], "Outgoing and incoming total for customer " + str(customer.get_id()) + " is wrong"


def gen_call(duration: int) -> Call:
    return Call("shit", "fuck", datetime.date(2000, 2, 2), duration, [1, 1], [1, 1])

def test_task3_term() -> None:
    contract = TermContract(datetime.date(2017, 1, 1),
                            datetime.date(2018, 1, 1))
    bill = Bill()
    contract.new_month(1, 2017, bill)
    assert bill.get_cost() == pytest.approx(320)
    contract.bill_call(gen_call(20 * 60))
    assert bill.get_cost() == pytest.approx(320)
    contract.bill_call(gen_call(20 * 60))
    assert bill.get_cost() == pytest.approx(320)
    contract.bill_call(gen_call(70 * 60))
    assert bill.get_cost() == pytest.approx(321)
    contract.bill_call(gen_call(100 * 60))
    assert bill.get_cost() == pytest.approx(331)

    bill = Bill()
    contract.new_month(2, 2017, bill)
    assert bill.get_cost() == pytest.approx(20)
    contract.bill_call(gen_call(150 * 60))
    assert bill.get_cost() == pytest.approx(25)

    assert contract.cancel_contract() == pytest.approx(25)

    contract = TermContract(datetime.date(2017, 1, 1),
                            datetime.date(2017, 2, 1))
    contract.new_month(1, 2017, Bill())
    contract.new_month(2, 2017, Bill())
    assert contract.cancel_contract() == pytest.approx(-280)


def test_task3_MTM() -> None:
    # MTM Contracts
    contract = MTMContract(datetime.date(2017, 2, 15))
    bill = Bill()
    contract.new_month(3, 2017, bill)
    assert bill.get_cost() == pytest.approx(50.0)
    contract.bill_call(gen_call(10))
    assert bill.get_cost() == pytest.approx(50.05)
    contract.bill_call(gen_call(50))
    assert bill.get_cost() == pytest.approx(50.1)
    bill = Bill()
    contract.new_month(4, 2017, bill)
    assert bill.get_cost() == pytest.approx(50.0)
    assert contract.cancel_contract() == pytest.approx(50.0)


def test_task3_prepaid() -> None:
    pass

def test_task4() -> None:
    # Filtering
    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    process_event_history(input_dictionary, customers)

    # Populate the list of calls:
    calls = []
    for customer in customers:
        hist = customer.get_history()
        calls.extend(hist[0])

    # The different filters we are testing

    # You need write LocationFilter test yourself
    filters = [
        DurationFilter(),
        CustomerFilter(),
        ResetFilter()
    ]

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    filter_strings = [
        ["L50", "G10", "L0", "50", "AA", "", "L100"],
        ["5555", "1111", "6020", "7930", "3087", "5524", "abc", ""],
        ["rrrr", ""]
    ]

    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [
        [122, 975, 0, 1000, 1000, 1000, 261],
        [1000, 1000, 59, 22, 22, 45, 1000, 1000],
        [1000, 1000]
    ]

    for i in range(len(filters)):
        for j in range(len(filter_strings[i])):
            result = filters[i].apply(customers, calls, filter_strings[i][j])
            assert len(result) == expected_return_lengths[i][j], str(filters[i].__class__.__name__) + ", with keyword " + filter_strings[i][j] + " produce wrong result"


def import_data() -> Dict[str, List[Dict]]:
    """ Open the file <dataset.json> which stores the json data, and return
    a dictionary that stores this data in a format as described in the A1
    handout.

    Precondition: the dataset file must be in the json format.
    """
    log = {}
    with open("dataset.json") as o:
        log = json.load(o)
    return log

test_dict_small = {'events': [
    {"type": "call",
     "src_number": "111-1111",
     "dst_number": "333-3333",
     "time": "2018-01-01 01:01:04",
     "duration": 10,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "222-2222",
     "dst_number": "333-3333",
     "time": "2018-01-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "333-3333",
     "dst_number": "111-1111",
     "time": "2018-01-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
    ],
    'customers': [
    {'lines': [
        {'number': '111-1111',
         'contract': 'term'},
        {'number': '222-2222',
         'contract': 'mtm'},
        {'number': '333-3333',
         'contract': 'prepaid'}
    ],
     'id': 8888}
    ]
}

test_dict_medium = {'events': [
    {"type": "call",
     "src_number": "111-1111",
     "dst_number": "333-3333",
     "time": "2018-01-01 01:01:04",
     "duration": 10,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "222-2222",
     "dst_number": "333-3333",
     "time": "2018-01-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "222-2222",
     "dst_number": "444-4444",
     "time": "2018-02-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "222-2222",
     "dst_number": "555-5555",
     "time": "2018-02-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "222-2222",
     "dst_number": "666-6666",
     "time": "2018-03-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "666-6666",
     "dst_number": "333-3333",
     "time": "2018-04-01 01:01:05",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]},
    {"type": "call",
     "src_number": "333-3333",
     "dst_number": "111-1111",
     "time": "2018-01-01 01:01:06",
     "duration": 50,
     "src_loc": [-79.42848154284123, 43.641401675960374],
     "dst_loc": [-79.52745693913239, 43.750338501653374]}
    ],
    'customers': [
    {'lines': [
        {'number': '111-1111',
         'contract': 'term'},
        {'number': '222-2222',
         'contract': 'mtm'},
        {'number': '333-3333',
         'contract': 'prepaid'}
    ],
     'id': 8888},
        {'lines': [
            {'number': '444-4444',
             'contract': 'term'},
            {'number': '555-5555',
             'contract': 'mtm'},
            {'number': '666-6666',
             'contract': 'prepaid'}
        ],
     'id': 6666},
    ]
}

if __name__ == '__main__':
    pytest.main(['a1_shitchecker_v3.py'])
