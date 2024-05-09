from django import forms
from .models import Mode, Language, Location, Authors, Collaborators, Producers, Educators, Stage, Sponsors, Topics, Course

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = '__all__'  # You can specify the fields you want to include in the form here

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'course_authors': forms.SelectMultiple(),
            'course_collab': forms.SelectMultiple(),
            'course_producers': forms.SelectMultiple(),
            'course_sponsors': forms.SelectMultiple(),
            'course_topic': forms.SelectMultiple(),
        }

from django import forms
from .models import Course_temp

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course_temp
        fields = '__all__'

