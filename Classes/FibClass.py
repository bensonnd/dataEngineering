class fib:
    '''Creates an iterable object that returns the values of the fib sequence up to the max'''
    def __init__(self,max):
        self.max = max

    def print_max(self):
        '''Member function'''
        print(self.max)

    def __iter__(self):
        '''iteration function to initialize first two values of fibinacci sequence'''
        self.a = 0
        self.b = 1
        return self

    def __next__(self):
        '''calculate the next two values in the fib sequence'''
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib

fib_obj = fib(10)

print([n for n in fib_obj])