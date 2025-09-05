from django.shortcuts import render, redirect
from .forms import  *
from .data_manager import load_data, save_data
import random


# Create your views here.
# from django.http import HttpResponse
# from django.template import loader

def home(request):
    context = {
        
    }
    return render(request, 'index.html', context)

def students(request):
    data = load_data()
    students = data.get("students", [])
    courses = data.get("courses", [])

    form = StudentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        
    # find the highest current ID:
    #get all the ids
        if students:
            ids = [obj['id'] for obj in students]
            highest_id = max(ids)
        else:
            highest_id = 0
        new_student = {
            "id": highest_id + 1,
            "name": form.cleaned_data["name"],
            "courses": []
        }

        # Add to course if selected
        selected_course_id = form.cleaned_data["course"]
        if selected_course_id:
            new_student["courses"].append(int(selected_course_id))

            # update that course’s student list
            for course in courses:
                if course["id"] == int(selected_course_id):
                    course.setdefault("students", []).append(new_student["id"])

        students.append(new_student)
        data["students"] = students
        data["courses"] = courses
        save_data(data)

        return redirect("students")

    return render(request, "students.html", {"form": form, "students": students})

def student_detail(request, student_id):
    data = load_data()
    students = data.get("students", [])
    courses = data.get("courses", [])

    student_id = int(student_id)
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        return redirect("students")
    
   

    # Make sure courses list is int
    student["courses"] = [int(c) for c in student.get("courses", [])]

    if request.method == "POST":
        
        print("posting")
        action = request.POST.get("action")
        course_id = int(request.POST.get("course_id"))
        
        print("DEBUG: action =", action, "course_id =", request.POST.get("course_id"))

        if action == "enroll" and course_id not in student["courses"]:
            student["courses"].append(course_id)
            

            for course in courses:
                if course["id"] == course_id:
                    course.setdefault("students", [])
                    if student["id"] not in course["students"]:
                        course["students"].append(student["id"])

        elif action == "remove" and course_id in student["courses"]:
            student["courses"].remove(course_id)

            for course in courses:
                if course["id"] == course_id:
                    course.setdefault("students", [])
                    course["students"] = [
                        sid for sid in course["students"] if sid != student["id"]
                    ]

        # Save after updates
        data["students"] = students
        data["courses"] = courses
        print(data)
        save_data(data)

        return redirect("students")

    return render(request, "individualStudent.html", {
        "student": student,
        "courses": courses,
        "student_courses": student["courses"],
    })



def courses(request):
    data = load_data()
    students = data.get("students", [])
    courses = data.get("courses", [])
    current_num = len(courses)

    form = CourseForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
         # find the highest current ID:
        #get all the ids
        if courses:
            ids = [obj['id'] for obj in courses]
            highest_id = max(ids)
        else:
            highest_id = 0
        
        new_course = {
            "id": highest_id + 1,
            "name": form.cleaned_data["name"],
            "students": [],
            "grades": [],
        }

        courses.append(new_course)
        data["students"] = students
        data["courses"] = courses
        save_data(data)

        return redirect("courses")

    return render(request, "courses.html", {"form": form, "courses": courses})

def course(request):
    return render(request, 'individualCourse.html')


def remove_student(request):
    data = load_data()
    students = data.get("students", [])
    courses = data.get("courses", [])

    if request.method == "POST":
        student_id = int(request.POST.get("student_id"))

        # Remove student from student list
        students = [s for s in students if s["id"] != student_id]

        # Also remove student from any course they were in
        for course in courses:
            if "students" in course:
                course["students"] = [sid for sid in course["students"] if sid != student_id]

        data["students"] = students
        data["courses"] = courses
        save_data(data)

        return redirect("students")

    return redirect("students")


def remove_course(request):
    data = load_data()
    students = data.get("students", [])
    courses = data.get("courses", [])

    if request.method == "POST":
        course_id = int(request.POST.get("course_id"))

        # Remove course from course list
        courses = [c for c in courses if c["id"] != course_id]

        # Also remove course from any students
        # for course in courses:
        #     if "students" in course:
        #         course["students"] = [sid for sid in course["students"] if sid != student_id]

        data["students"] = students
        data["courses"] = courses
        save_data(data)

        return redirect("courses")

    return redirect("courses")
    
