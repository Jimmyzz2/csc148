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
import datetime
from typing import Optional
from math import ceil
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This is an abstract class. Only subclasses should be instantiated.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()

class TermContract(Contract):
    """ A term based contract for a phone line

    This is a subclasses of Contract.

    === Public Attributes ===
    start:
         starting date for the contract
    end:
        ending date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset

    === Private Attributes ===
    _month:
        current month value passed in by new_month method
    _year:
        current year value passed in by new_month method
    """
    start: datetime.datetime
    end: datetime.datetime
    bill: Optional[Bill]
    _month: int
    _year: int

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """ Create a new Term Contract with the <start> date, starts as inactive
        """
        Contract.__init__(self, start)
        self.end = end
        self._month = 0
        self._year = 0

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the Term contract, corresponding
        to <month> and <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the
        appropriate rate per minute and fixed cost.

        """
        # case not first month of contract
        if self.start.month != month or self.start.year != year:
            # set rate per minute and fixed cost
            self.bill = bill
            self.bill.set_rates("TERM", 0.1)
            self.bill.add_fixed_cost(20.00)
            self._month = month
            self._year = year
            # case first month of contract, pay deposit
        else:
            self.bill = bill
            self.bill.set_rates("TERM", 0.1)
            self.bill.add_fixed_cost(320.00)
            self._month = month
            self._year = year

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        if self.bill.free_min <= 100:
            add_free = self.bill.free_min + (ceil(call.duration/60))
            if add_free <= 100:
                self.bill.add_free_minutes(ceil(call.duration/60))
            else:
                self.bill.add_free_minutes(100 - self.bill.free_min)
                self.bill.add_billed_minutes(add_free - 100)
        # exceeds free minutes
        else:
            self.bill.add_billed_minutes(ceil(call.duration/60))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this Term contract. The canecelation date is the first date of
        last month-year combination in the dataset.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        # calculate cancel date which is
        # last month year combination in the data set
        cancel_date = datetime.date(self._year, self._month, 1)
        # case deposit is gone
        if cancel_date < self.end:
            self.start = None
            self.end = None
            return self.bill.get_cost()
        # case deposit back
        else:
            self.start = None
            self.end = None
            money = self.bill.get_cost() - 300
            return money
        # net difference (can be positive or negative)


class MTMContract(Contract):
    """ A month-to-month contract for a phone line

    This is a subclass of Contract.


    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Month to Month Contract with the
        <start> date, starts as inactive
        """
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the Month to Month contract,
        corresponding to <month> and <year>. This may be
        the first month of the contract.
        Store the <bill> argument in this contract
        and set the appropriate rate
        per minute and fixed cost.
        """
        self.bill = bill
        self.bill.set_rates("MTM", 0.05)
        self.bill.add_fixed_cost(50.00)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration/60))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this Month to Month contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class PrepaidContract(Contract):
    """ A prepaid contract for a phone line

    This is an subclass of Contract.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset

    === Private Attributes ===
    _balance:
        The amount of money this customer have in account. Negative indicates
        credit, and positive indicates owned amount
    """
    start: datetime.date
    bill: Optional[Bill]
    _balance: float

    def __init__(self, start: datetime.date, balance: float) -> None:
        """ Create a new Prepaid Contract with the
        <start> date, starts as inactive
        """
        # when signing up, the customer must prepay some amount,
        # but can be any amount
        Contract.__init__(self, start)
        self._balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the Prepaid contract,
        corresponding to <month> and <year>. Inherit balance from last month.
        This may be the first month of the contract.
        Store the <bill> argument in this contract
        and set the appropriate rate per minute and fixed cost.
        """
        # case not first month of contract
        if self.start.month != month or self.start.year != year:
            # set rate per minute and fixed cost
            # carry over balance
            if self.bill is not None:
                self._balance = self.bill.get_cost()
            # if less than 10 credit, the balance must get a top-up of 25
            if self._balance > -10:
                self._balance -= 25
            # self._balance -= 25 bc it wont take effect this month, but will be
            # taking effect next month
            self.bill = bill
            self.bill.set_rates("PREPAID", 0.025)
            self.bill.add_fixed_cost(self._balance)
        # case first month of contract
        else:
            self.bill = bill
            self.bill.set_rates("PREPAID", 0.025)
            # subtract prepaid from the bill cost
            self.bill.add_fixed_cost(self._balance)
            # less than 10 credit, the balance must get a top-up of 25
            if self._balance > -10:
                self._balance -= 25

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration/60))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this Prepaid contract. Return 0 if balance has credits left.
        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        balance = self.bill.get_cost()
        # when balance is positive indicates customer owes money to the company
        # and the left credit is forheited
        if balance > 0:
            return balance
        else:
            return 0




if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
