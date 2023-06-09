#!/usr/bin/env python3

class Person:
    def __init__(self, name, age):
        self.name = name 
        self.age = age 

    def __repr__(self):
        return f"{self.name} is {self.age} years old."

    def __eq__(self, other):
        return isinstance(other, Person)

class Dog:
    def __init__(self, name, age):
        self.name = name 
        self.age = age 

    def __str__(self):
        return f"{self.name} is {self.age} years old."

def main():
    person = Person("Joe Biden", 80)
    print(person)  # prints "Joe Biden is 80 years old."
    print(str(person)) # prints "Joe Biden is 80 years old." i.e. __repr__ overrides __str__
    print(repr(person)) # prints "Joe Biden is 80 years old."

    dog = Dog("Spot", 5)
    print(dog) # prints "Spot is 5 years old."
    print(str(dog)) #prints "Spot is 5 years old."
    print(repr(dog)) # prints <__main__.Dog object at 0x7f117b592080> i.e __str__ does not override __repr__

    person2 = Person("Barack Obama", 61)

    print(person == person2) #Prints True because we used __eq__, even if this may not really make sense
    print(person == dog) #Prints False

if __name__ == "__main__":
    #explanation in assignment5.pdf
    main()