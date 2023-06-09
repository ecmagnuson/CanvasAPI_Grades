#!/usr/bin/env python3

import json
import os
import pathlib
import shutil
import sys
import urllib.request
from dataclasses import dataclass

from canvasapi import Canvas

def validate():
    #Validate the url and key and return a canvas object
    with open("auth.txt", "r") as f:
        d = json.load(f)
    try:
        API_URL = d["API_URL"]
        API_KEY = d["API_KEY"]
        return Canvas(API_URL, API_KEY)
    except KeyError:
        print('There was an error accessing the API_URL or API_KEY inside of the "auth.txt" file.')
        print("Enter each inside of double quotes, i.e.")
        print('"https://canvas.wisc.edu/"')
        sys.exit(1)

def get_a_course(canvas):
    #return a Course object that the user picked
    courses = active_canvas_courses(canvas)
    print(f"There are {len(courses)} active courses in your Canvas page in which you are a teacher.")
    print('''Note: Some old classes may be listed here. 
    If they are, that means they are still listed as active under Canvas.\n''')
    for i, course in enumerate(courses):
        print(f"({i}) --" , course.name)
    while True:
        try:
            print("\nWhich class would you like to choose?")
            choice = int(input("> "))
            if choice < 0: continue
            print()
            return courses[choice]
        except (ValueError, IndexError):
            print("Enter a digit corresponding to the course")

def active_canvas_courses(canvas):
    #return a list of all active Canvas courses which you are a ta or teacher
    current = []
    courses = canvas.get_courses()
    types = ["teacher", "ta"]
    for course in courses:
        try:
            #TODO this is pretty ugly, but ok for now..
            if ( 
                # One enrollment is a list of one dict
                course.enrollments[0]["enrollment_state"] == "active" 
                and 
                course.enrollments[0]["type"] in types
            ):
                current.append(course)    
        except AttributeError:
            #There is a strange issue where old Canvas classes raise this error, idk why..
            pass       
    return current   

def get_course_section(course):
    #return a Section object corresponding to the user input
    sections = course.get_sections()
    for i, section in enumerate(sections):
        print(f"({i}) --" , section)
    while True:
        try:
            print(f"\nWhat section of {course.name} do you want to get?")
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

def group_id2name(course):
    d = {}
    for group in course.get_groups():
        d[group.id] = group.name
    return d

@dataclass
class Student: 
    name: str
    ID: str
    group: str

def get_section_students(section, groups):
    #return a list of Student objects (name, id, group_name) in the desired section
    section_students = []
    enrollments = section.get_enrollments(include='group_ids')
    for enrollment in enrollments:
        if enrollment.role == "StudentEnrollment":
            name = enrollment.user["name"].title().replace(" ", "")
            ID = enrollment.user["id"]
            group_ID = enrollment.user["group_ids"]
            try:
                group_name = groups[(group_ID[0])]
            except IndexError:
                section_students.append(Student(name, ID, "unassigned_group"))
                continue
            section_students.append(Student(name, ID, group_name))
    return section_students

def get_published_assignments(course):
    #Return a list of assignments for the course that are published
    #TODO this hangs for a bit
    assignments = course.get_assignments()
    published_assignments = []
    [published_assignments.append(a) for a in assignments if a.published]
    for i, assignment in enumerate(published_assignments):
        print(f"({i}) --" , assignment.name)
    while True:
        try:
            print("\nHere are all of the published assignments to the class.")
            print("What assignment do you want to download the files for?")
            choice = int(input("> "))
            if choice < 0: continue
            return published_assignments[choice]
        except (ValueError, IndexError):
            print("Enter a digit corresponding to the published assignment.")

def move_resources(student_dir):
    #Move all of the resources in the resource directory into the student_dir
    name = student_dir.split("/")[-1]
    try:
        resources = os.listdir("./resources")
        for r in resources:
            shutil.copyfile("./resources/" + r, student_dir + "/" + name + r)
    except FileNotFoundError:
        return 

def prepare_directory(student, assignment_name):
    #TODO quick rework.. refactor this
    group_dir = f"./submissions/{assignment_name}/{student.group}"
    os.makedirs(group_dir, exist_ok=True)
    student_dir = f"{group_dir}/{student.name}"
    os.makedirs(student_dir, exist_ok=True)
    move_resources(student_dir)
    return student_dir

def download_submissions(students, assignment):
    #downloads assignments into ./submissions directory
    print("\nWhat do you want to call the name of the file for each student?")
    assignment_name = input("> ")
    os.makedirs("./submissions/" + assignment_name, exist_ok=True)
    print()
    for i, student in enumerate(students, 1):
        submissions = assignment.get_submission(student.ID).attachments
        if len(submissions) == 0:
            print(f"No submission from {student.name}\n")
            continue
        student_dir = prepare_directory(student, assignment_name)
        if len(submissions) == 1:
            #print(str(submissions)[0])
            extension = pathlib.Path(str(submissions[0])).suffixes[-1] 
            title = f"{student_dir}/{student.name}_{assignment_name}{extension}"
            urllib.request.urlretrieve(submissions[0].url, title)
        else:
            print(f"{student.name} appears to have {len(submissions)} submissions for this assignment")
            print("Defaulting to original student file names..\n")
            for sub in submissions:
                extension = pathlib.Path(str(sub)).suffixes[-1] 
                title = f"{student_dir}/{student.name}_{str(sub)}"
                urllib.request.urlretrieve(sub.url, title)
        print(f"downloading submission {i} of {len(students) - 1} students", end = "\r")
        sys.stdout.write("\033[K") # Clear to the end of line
    path = os.path.join(check_using_pyinstaller(), "submissions", assignment_name)
    print(f"Files have been downloaded to {path}")

def check_using_pyinstaller():
    #return the current location script is executing from
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        return application_path
    return os.path.dirname(os.path.abspath(__file__))

def main():
    canvas = validate()
    course = get_a_course(canvas)
    id2name = group_id2name(course)
    section = get_course_section(course)
    section_students = get_section_students(section, id2name)
    assignment = get_published_assignments(course)
    download_submissions(section_students, assignment)

if __name__ == "__main__":
    sys.exit(main())
