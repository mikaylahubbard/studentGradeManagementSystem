from django import forms
from .data_manager import load_data

class StudentForm(forms.Form):
    name = forms.CharField(label="Student Name", max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = load_data()
        courses = data.get("courses", [])
        choices = [("", "----")] + [(c["id"], c["name"]) for c in courses]
        self.fields["course"] = forms.ChoiceField(
            label="Enroll in Course (optional)",
            choices=choices,
            required=False
        )
        


class CourseForm(forms.Form):
    name = forms.CharField(label="Course Name", max_length=100)

        