from django.urls import path
from . import views

app_name = 'tools'  # Register the 'tools' namespace

urlpatterns = [
    path('exam-generator/', views.generate_exams_view, name='exam_generator_view'),
]
