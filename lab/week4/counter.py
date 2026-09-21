class MyCounter(object):
    def __init__(self, high, low=1):
        self.high = high
        self.low = low
        self.current = low

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        self.current += 1
        return self.current - 1

    def reset(self):
        self.current = self.low

    def set_range(self, low, high):
        self.high = high
        self.low = low
        self.reset()

    def set_low(self, low):
        self.low = low
        self.reset()

    def set_high(self, high):
        self.high = high
        self.reset()

    def __len__(self):
        return self.high - self.low + 1
    
    def __repr__(self):
        return f"MyCounter(low={self.low}, high={self.high}, current={self.current})"
    def __str__(self):
        return f"MyCounter(low={self.low}, high={self.high}, current={self.current})"

    def __sum__(self):
        """Return the sum of the counter's values without consuming it."""
        return sum(range(self.low, self.high + 1))

def test_my_counter():
    counter = MyCounter(high=15)
    print(counter, ":", len(counter))
    print("Sum of counter:", sum(counter))  
    print("Sum of (1,2,3):", sum((1,2,3)))
    for i in counter:
        print(i)

    
    counter.reset()
    print("After reset:", counter)
    for i in counter:
        print(i)
    counter.set_range(5, 15)
    print("After setting range to 5-15:", counter)
    counter.set_low(8)  
    print("After setting low to 8:", counter)
    print("Length of counter:", len(counter))
    print("Representation of counter:", repr(counter))
    print("String of counter:", str(counter))
    print("Iterating again after reset:")
    counter.reset()
    for i in counter:
        print(i)


if __name__ == "__main__":
    test_my_counter()
