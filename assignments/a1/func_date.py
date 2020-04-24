def func(year, month, new):
    month = month + new
    year = year
    if month > 12:
        if month % 12 == 0:
            year += month // 12 - 1
            month = month % 12 + 12
        else:
            year += month // 12
            month = month % 12
    return [year, month]


def minus(year1, month1, year2, month2):
    """
    Return month date1 minus date2
    Precondition date1 > date2
    """
    if month1 >= month2:
        month = month1 - month2 + (year1 - year2) * 12
    if month1 <= month2:
        month = month1 + 12 - month2 + (year1 - 1 - year2) * 12
    return month


