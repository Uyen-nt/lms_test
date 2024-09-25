from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
from .forms import CourseForm
from module_group.models import ModuleGroup

def course_list(request):
    module_groups = ModuleGroup.objects.all()
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses, 'module_groups': module_groups})

def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course:course_list')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')
    return render(request, 'course_confirm_delete.html', {'course': course})
