# import counter as ct
# from mod1.counter import MyCounter 
from counter import MyCounter 

def main():
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
    print("Sum of counter using __sum__:", counter.__sum__())

if __name__ == "__main__":
    main() 