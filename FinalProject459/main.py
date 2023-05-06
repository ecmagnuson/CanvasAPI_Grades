#!/usr/bin/env python3

import os 
import urllib.request
import shutil
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

def wants_sections():
    # Ask the user if they want the group information
    while True:
        answer = input("Do you want a specific section from this class? (y/n) ")
        if answer == "y":
            return True
        elif answer == "n":
            return False

def get_a_section(course_id):
    #return a Section object corresponding to the user input
    print() # NOTE just to make spacing look nicer, but this is ugly
    sections = get_sections(course_id)
    for i, section in enumerate(sections):
        print(f"({i}) --" , section["name"])
    while True:
        try:
            print(f"\nWhat section do you want to get?")
            choice = input("> ")
            print()
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

@dataclass(eq=True, unsafe_hash=True)
class Student :
    # An object representing some useful attributes for each student
    name: str 
    u_id: str 
    group_ids: list[str]
    chosen_group_name: str
    submission_attatchments: list[dict[str, str]]

def all_students(course_id):
    # Get all student enrollments for a course
    # url:GET|/api/v1/courses/:course_id/enrollments
    # For some really weird reason when I make this url request it is 
    # duplicating all of the students. I have no idea why.
    # This needs to use Pagination because it exceeds the limit of 100 per_page
    # https://canvas.instructure.com/doc/api/file.pagination.html
    c = CanvasRequests(f"/courses/{course_id}/enrollments")
    params = { 
        "type": ["StudentEnrollment"],
        "include": ["group_ids"],
        "per_page": "100"
    } 
    enrollments = []
    while c.full_url:
        response = c.get(**params) # TODO Figure out why does this GET request duplicate every student??
        enrollment_response = response.json() 
        enrollments.extend(enrollment_response)
        c.full_url = response.links.get("next", {}).get("url", None)
    students = populate_students(enrollments)
    temp = [] 
    [temp.append(x) for x in students if x not in temp]
    return temp

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
    students = populate_students(enrollments)
    return students

def populate_students(enrollments):
    # create the Student dataclass objects from a list of enrollements
    students = []
    for e in enrollments:
        user = e["user"]
        name = user["name"]
        #Format name!
        name = name.title().replace(" ", "")
        u_id = user["id"]
        group_ids = user["group_ids"]
        students.append(Student(name,u_id,group_ids,"no_group",[]))
    return students

def wants_groups():
    # Ask the user if they want the group information
    while True:
        answer = input("Do you want the groups? (y/n) ")
        if answer == "y":
            return True
        elif answer == "n":
            return False

def get_group_categories(course_id):
    # Get the group categories from a course
    # url:GET|/api/v1/courses/:course_id/group_categories
    c = CanvasRequests(f"/courses/{course_id}/group_categories")
    groups = c.get().json()
    return groups

def get_a_group_category(course_id):
    # return a group category corresponding to the users choice
    groups = get_group_categories(course_id)
    print() #NOTE another blank print for spacing
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

def get_an_assignment(course_id):
    published_assignments = get_assignments(course_id)
    for i, assignment in enumerate(published_assignments):
        print(f"({i}) --" , assignment["name"])
    while True:
        try:
            print("\nHere are all of the published assignments to the class that are ungraded.")
            print("What assignment do you want to download the files for?")
            choice = int(input("> "))
            if choice < 0: continue
            return published_assignments[choice]
        except (ValueError, IndexError):
            print("Enter a digit corresponding to the published assignment.")

def get_assignments(course_id):
    # Return a list of assignments for the course that are published and ungraded
    # url:GET|/api/v1/courses/:course_id/assignments
    c = CanvasRequests(f"/courses/{course_id}/assignments")
    params = {
        "per_page": "100",
        "bucket": "ungraded" # Won't show assignments that are already graded
    }
    all_assignments = c.get(**params).json() 
    published_assignments = []
    for a in all_assignments:
        # I only care about published assignements with points > 0
        if a["published"] and a["points_possible"] > 0:
            published_assignments.append(a)
    return published_assignments

def populate_student_submissions(students, assignment, course_id):
    # For a given assignment, populate all students submission_attatchments attribute
    # :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id
    assignment_id = assignment["id"]
    chosen_dir_name = prompt_directory_name()
    for s in students:
        #submissions = assignment.get_submission(student.ID).attachments
        c = CanvasRequests(f"/courses/{course_id}/assignments/{assignment_id}/submissions/{s.u_id}")
        submissions = c.get().json() 
        try:   
            # If there is no attatchment (student didn't submit) for this assignment it will crash
            attatchements = submissions["attachments"]
        except KeyError:
            continue
        for a in attatchements:
            display_name = a["display_name"]
            url = a["url"]
            mime_class = a["mime_class"] # pdf, doc, etc 
            s.submission_attatchments.append(
                {
                    "display_name": display_name,
                    "url": url,
                    "mime_class": mime_class
                } 
            )
        group_dir = prepare_group_directory(s, chosen_dir_name)
        download_submission(s, group_dir, chosen_dir_name) #TODO this is way overly complicated..

def download_submission(student, group_dir, dir_name):
    # Download the submissions from one student for an assignment
    # The student object already has access to the urls, assignment, etc.
    # downloads assignments into ./submissions/{group_dir} directory
    # Also moves resources to the student path
    attatchments = student.submission_attatchments
    student_path = f"{group_dir}/{student.name}"
    move_resources(student_path)
    if len(attatchments) == 1: # If only one attatchment then can rename
        extension = attatchments[0]["mime_class"] # .docx, .pdf, etc
        file_path = f"{student_path}/{student.name}_{dir_name}.{extension}"
        url = attatchments[0]["url"]
        urllib.request.urlretrieve(url, file_path)
        message = f"Downloading assignment for {student.name}"
        print(message)
        sys.stdout.write("\033[K") # Clear to the end of line
    else:
        for a in attatchments: # Default to original name if more than 1 attatchment
            file_name = a["display_name"]
            file_path = f"{student_path}/{file_name}"
            url = a["url"]
            urllib.request.urlretrieve(url, file_path)
            message = f"{student.name} has more than 1 attatchment for this assignment, defaulting to original submission names."
            print(message)
            sys.stdout.write("\033[K") # Clear to the end of line

def prepare_group_directory(student, dir_name):
    group_dir = f"./submissions/{dir_name}/{student.chosen_group_name}"
    os.makedirs(f"{group_dir}/{student.name}", exist_ok=True)
    return group_dir

def prompt_directory_name():
    # Promp the user for a directory name 
    print("\nWhat do you want the renamed submissions to be named?")
    dir_name = input("> ")
    return dir_name

def move_resources(student_dir):
    #Move all of the "~./resources" in the resource directory into the student_dir
    name = student_dir.split("/")[-1]
    try:
        resources = os.listdir("./resources")
        for r in resources:
            shutil.copyfile(f"./resources/{r}", f"{student_dir}/{name}_{r}")
    except FileNotFoundError:
        return 

def main():
    course = get_a_course() # Initial prompt asking for class

    if wants_sections(): #Get only students from 1 section
        section = get_a_section(course["id"])
        students = section_students(section["id"])
    else: # Get all students
        students = all_students(course["id"])

    if wants_groups(): # Get group info for each student
        group_category = get_a_group_category(course["id"])
        groups = get_groups(group_category["id"])
        g_id2name = group_id2name(groups)
        populate_group_name(students, groups, g_id2name)

    # Now have a list of students
    # Either all students or students in one section
    # Either groups or no groups 

    assignment = get_an_assignment(course["id"])
    populate_student_submissions(students, assignment, course["id"])

if __name__ == "__main__":
    main()