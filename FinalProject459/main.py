#!/usr/bin/env python3

import json
import os
import requests
import sys

def credentials():
    # Get the API_URL and API_KEY for canvas credentials
    auth = os.path.join(os.path.dirname(__file__), 'auth.json')
    with open(auth, "r") as f:
        d = json.load(f)
    return d

def get_courses():
    # Get a list of all of the active canvas class which you are a teacher
    d = credentials()
    API_URL = d["API_URL"]
    API_KEY = d["API_KEY"]
    headers = {"Authorization": "Bearer " + API_KEY}
    url = f"{API_URL}/courses"
    params = { #API https://canvas.instructure.com/doc/api/courses.html
        "enrollment_type": "teacher", 
        "enrollment_state": "active", 
        "include": ["sections"]
    }
    response = requests.get(url, headers=headers, params=params)
    courses = response.json()
    return courses

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

def get_section(course_id):
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
    d = credentials()
    API_URL = d["API_URL"]
    API_KEY = d["API_KEY"]
    headers = {"Authorization": "Bearer " + API_KEY}
    url = f"{API_URL}/courses/{course_id}/sections"
    response = requests.get(url, headers=headers)
    sections = response.json()
    return sections

def main():
    # get the course you want
    # ask if you want a specific section or all sections?
    # check if groups?
    # get the assignments
    # download the assignments
    
    course = get_a_course()
    section = get_section(course["id"])

    if section is not None:
        print(section["name"])

    
if __name__ == "__main__":
    sys.exit(main())
