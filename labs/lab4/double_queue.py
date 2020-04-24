from myqueue import Queue
class DoubleQueue(Queue):


    def __init__(self, is_special):
        Queue.__init__(self)
        self.function = is_special

    def enqueue(self, item):
        Queue.enqueue(self, item)
        if self.function(item):
            Queue.enqueue(self, item)


