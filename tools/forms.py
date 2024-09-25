# forms.py
from django import forms

class ExamGenerationForm(forms.Form):
    excel_file = forms.FileField(label="Upload Excel File")
    number_of_exams = forms.IntegerField(label="Number of Exams", min_value=1, max_value=100, initial=1)
