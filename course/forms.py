from django import forms
from .models import Course  # Model của bạn

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_description', 'subject']  # Các trường của khóa học
        widgets = {
            'subject': forms.Select(),
        }
