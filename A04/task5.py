#!/usr/bin/env python3

class Student:

    def __init__(self, lastName = "Popescu", gpa = 3.8):
        if (isinstance(float(gpa), float)) and (gpa <= 4 and gpa >= 0):
            self.gpa = gpa
        else:
            print("gpa must be set to a float between 0 and 4. Defaulting to a gpa of 3.8")
            self.gpa = 3.8
        
        if (isinstance(lastName, str)):
            self.lastName = lastName
        else:
            print("lastName must be a string. Defaulting to 'Popescu'")
            self.lastName = "Popescu"

    def compareGPA(self, s_other):
        highest_grade = max(self.gpa, s_other.gpa)
        if self.gpa == s_other.gpa:
            print(f"Both {self.lastName} and {s_other.lastName} have the same grade")
        elif self.gpa == highest_grade:
            print(self.lastName)
        else:
            print(s_other.lastName)
