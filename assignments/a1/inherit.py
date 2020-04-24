class A:
    def __init__(self, m):
        self.m = m

    def ace(self):
        return self.m + 1

class B(A):
    def __init__(self, m):
        A.__init__(self, m)
