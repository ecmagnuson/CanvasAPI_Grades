#!/usr/bin/env python3

import json
import os
import requests
import sys

from canvas import CanvasRequests

def get_a_course():
    #return a Course object that the user picked
    courses = get_courses()
    print(f"There are {len(courses)} active courses in your Canvas page in which you are a teacher.")
    for i, course in enumerate(courses):
        print(f"({i}) --" , course["name"])
    while True:
        try:
            print("\nWhich class would you like to choose?")
            choice = int(input("> "))
            if choice < 0: continue
            print()
            return courses[choice]
        except (ValueError, IndexError):
            print("Enter a digit corresponding to the course")

def get_courses():
    # Get a list of all of the active canvas class which you are a teacher
    # https://canvas.instructure.com/doc/api/courses.html
    # url:GET|/api/v1/courses
    c = CanvasRequests()
    params = { 
            "enrollment_type": "teacher", 
            "enrollment_state": "active", 
    }   
    courses = c.get(**params).json()
    return courses

def get_a_section(course_id):
    #return a Section object corresponding to the user input
    sections = get_sections(course_id)
    for i, section in enumerate(sections):
        print(f"({i}) --" , section["name"])
    while True:
        try:
            print(f"\nWhat section do you want to get?")
            print("You can leave this blank if you want to get all sections.")
            choice = input("> ")
            print()
            if choice == "":
                # No desired section
                return None
            else:
                #choice = int(choice) # TODO this is a bit hacky
                return sections[int(choice)]
        except (ValueError, IndexError):
            print("Enter a digit corresponding to the section")

def get_sections(course_id):
    # Get a list of all of the sections for a specific course
    # https://canvas.instructure.com/doc/api/sections.html
    # url:GET|/api/v1/courses/:course_id/sections
    c = CanvasRequests(f"/{course_id}/sections")
    sections = c.get().json()
    return sections

def get_all_students(course_id):
    # Get a list of all of the students in a course
    #url:GET /api/v1/courses/:course_id/search_users 
    c = CanvasRequests(f"/{course_id}/users")
    params = { 
        "enrollment_state": ["active"],
        "enrollment_type": ["student"],
        "per_page": "100" # Defaults to 10 if not set.
        #Need to change if more than 100 students
    }   
    students = c.get(**params).json()
    return students

def get_section_students(course_id, section_id):
    # Get a list of a specific section in a course
    # url:GET|/api/v1/courses/:course_id/sections/:id
    c = CanvasRequests(f"/{course_id}/sections/{section_id}")
    params = { 
        "include": ["enrollments", "students"]
    }  
    section_info = c.get(**params).json()
    students = section_info["students"]
    return students

def main():
    # get the course you want
    # ask if you want a specific section or all sections?
    # check if groups?
    # get the assignments
    # download the assignments
    
    course = get_a_course()
    section = get_a_section(course["id"])

    if section is not None:
        students = get_section_students(course["id"], section["id"])
    else:
        students = get_all_students(course["id"])

    for s in students:
        print(s["name"])
    
if __name__ == "__main__":
    sys.exit(main())