#!/usr/bin/env python3

import json
import os
import requests
import sys
from dataclasses import dataclass

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
    c = CanvasRequests("/courses")
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
    c = CanvasRequests(f"/courses/{course_id}/sections")
    sections = c.get().json()
    return sections

@dataclass
class Student:
    # An object representing some useful attributes for each student
    name: str 
    u_id: str 
    group_ids: list[str]
    chosen_group_name: str

def all_students(course_id):
    # Get all student enrollments for a course
    # url:GET|/api/v1/courses/:course_id/enrollments
    c = CanvasRequests(f"/courses/{course_id}/enrollments")
    params = { 
        "type": ["StudentEnrollment"],
        "include": ["group_ids"],
        "per_page": "500"
    } 
    enrollments = c.get(**params).json() 
    students = populate_student(enrollments)
    return students

def section_students(section_id):
    # Get student enrollments for one section.
    # url:GET|/api/v1/sections/:section_id/enrollments
    c = CanvasRequests(f"/sections/{section_id}/enrollments")
    params = { 
        "type": ["StudentEnrollment"],
        "include": ["group_ids"],
        "per_page": "100"
    } 
    enrollments = c.get(**params).json() 
    students = populate_student(enrollments)
    return students

def populate_student(enrollments):
    # create the Student dataclass objects from a list of enrollements
    students = []
    for e in enrollments:
        user = e["user"]
        name = user["name"]
        u_id = user["id"]
        group_ids = user["group_ids"]
        students.append(Student(name,u_id,group_ids,"unknown"))
    return students

def wants_groups():
    # Ask the user if they want the group information
    while True:
        answer = input("Do you want the groups? (y/n)")
        if answer == "y" or answer == "n":
            return answer

def get_group_categories(course_id):
    # Get the group categories from a course
    # url:GET|/api/v1/courses/:course_id/group_categories
    c = CanvasRequests(f"/courses/{course_id}/group_categories")
    groups = c.get().json()
    return groups

def get_a_group_category(course_id):
    # return a group category corresponding to the users choice
    groups = get_group_categories(course_id)
    for i, group in enumerate(groups):
        print(f"({i}) --" , group["name"])
    while True:
        try:
            print(f"\nWhat group do you want to get?")
            choice = input("> ")
            print()
            return groups[int(choice)]
        except (ValueError, IndexError):
            print("Enter a digit corresponding to the section")

def get_groups(group_category_id):
    # Get all of the groups in a group category
    # url:GET|/api/v1/group_categories/:group_category_id/groups
    c = CanvasRequests(f"/group_categories/{group_category_id}/groups")
    params = {
        "per_page": "100"
    }
    groups = c.get(**params).json() 
    return groups

def group_id2name(groups):
    d = {}
    for group in groups:
        d[group["id"]] = group["name"]
    return d

def populate_group_name(students, groups , g_id2name):
    #for each students group_ids we want to find the name for that group
    # This is really bad doing it this way
    # Fortunately in my case it is not that much to loop over
    for s in students:
        for g_id in s.group_ids:
            for g in groups:
                if g_id == g["id"]:
                    s.chosen_group_name = g_id2name[g_id]

def user_group_category():
    # url:GET|/api/v1/group_categories/:group_category_id/users
    pass 

def main():
    # get the course you want
    # ask if you want a specific section or all sections?
    # check if groups?
    # group id2name

    # get the assignments
    # download the assignments
    
    course = get_a_course()
    section = get_a_section(course["id"])

    if section is not None:
        students = section_students(section["id"])
    else:
        students = all_students(course["id"])

    answer = wants_groups()

    if answer == "y":
        group_category = get_a_group_category(course["id"])
        groups = get_groups(group_category["id"])
        g_id2name = group_id2name(groups)
        populate_group_name(students, groups, g_id2name)

if __name__ == "__main__":
    sys.exit(main())