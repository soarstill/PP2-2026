capitals ={"Korea":"Seoul","USA":"Washington","UK":"London"} 

city = capitals.pop("UK")
print(capitals)

if "UK"in capitals :
	capitals.pop("UK")

capitals.clear()
if len(capitals)==0 :
	print("딕셔너리에 항목이 있음")
else:
	print("딕셔너리가 비어 있음")

for key in capitals :
        print( key, end=" ")

capitals ={"Korea":"Seoul","USA":"Washington","UK":"London"} 
for key in capitals :
        print( key,":", capitals[key])
