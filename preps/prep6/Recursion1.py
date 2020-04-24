def sum_nested(obj):
    if isinstance(obj, int):
        return obj
    else:
        s = 0
        for sublist in obj:
            s += sum_nested(sublist)
        return s


# wont create error even the input is []
#(0) a = []
#(1) bc for i in a:
#(2)        print('x')
# does not go to the second line