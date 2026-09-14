class Person():
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name


Person 클래스
Student 클래스
    def isStudent(self):
        return False
   
class Student(Person):
   def __init__(self, name, gpa):
       super().__init__(name)
       self.gpa = gpa

   def isStudent(self):
        return True
   
obj1 = Person("Kim")  
print(obj1.getName(), obj1.isStudent())
   
obj2 = Student("Park", 4.3) 
print(obj2.getName(), obj2.isStudent())
