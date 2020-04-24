
class A:
    def koo(self):
        print('goo')

    def noo(self):
        A.koo(self)


class B(A):
    def koo(self):
        print('goo2')
