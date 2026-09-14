a = 0b00001101
b = 0b00001010
print( a&b, a|b, a^b )
print( bin(a&b), bin(a|b), bin(a^b) )

a = 0b00001101
print(~a, bin(~a))

a = 0b00001101
print(~a&255, bin(~a&255))
