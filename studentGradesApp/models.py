from django.db import models

# Create your models here.
# app/models.py (not using Django ORM, just Python classes)

class Student:
    def __init__(self, id, name, courses=None):
        self.id = id
        self.name = name
        self.courses = courses if courses else []  # list of Course IDs

class Course:
    def __init__(self, id, name, students=None, grades=None):
        self.id = id
        self.name = name
        self.students = students if students else []  # list of Student IDs
        self.grades = grades if grades else {}  # {student_id: grade}
