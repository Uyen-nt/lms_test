from django.db import models
from subject.models import Subject

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_description = models.TextField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.course_name  # Should return course_name instead of username
