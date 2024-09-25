# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Module, ModuleGroup
from .forms import ModuleForm, ModuleGroupForm

# ModuleGroup views
def module_group_list(request):
    module_groups = ModuleGroup.objects.all()
    return render(request, 'module_group_list.html', {'module_groups': module_groups})

def module_group_detail(request, pk):
    module_group = get_object_or_404(ModuleGroup, pk=pk)
    return render(request, 'module_group_detail.html', {'module_group': module_group})

def module_group_add(request):
    if request.method == 'POST':
        form = ModuleGroupForm(request.POST)
        if form.is_valid():
            print("Form data:", form.cleaned_data)  # Debugging line
            form.save()
            return redirect('module_group:module_group_list')
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = ModuleGroupForm()
    return render(request, 'module_group_form.html', {'form': form})


def module_group_edit(request, pk):
    module_group = get_object_or_404(ModuleGroup, pk=pk)
    if request.method == 'POST':
        form = ModuleGroupForm(request.POST, instance=module_group)
        if form.is_valid():
            form.save()
            return redirect('module_group:module_group_list')
    else:
        form = ModuleGroupForm(instance=module_group)
    return render(request, 'module_group_form.html', {'form': form})

def module_group_delete(request, pk):
    module_group = get_object_or_404(ModuleGroup, pk=pk)
    if request.method == 'POST':
        module_group.delete()
        return redirect('module_group:module_group_list')
    return render(request, 'module_group_confirm_delete.html', {'module_group': module_group})

# MODULE
def module_list(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    return render(request, 'module_list.html', {'module_groups': module_groups,'modules': modules})

def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    return render(request, 'module_detail.html', {'module': module})

def module_add(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_group:module_list')
    else:
        form = ModuleForm()
    return render(request, 'module_form.html', {'form': form})

def module_edit(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_group:module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'module_form.html', {'form': form})

def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('module_group:module_list')
    return render(request, 'module_confirm_delete.html', {'module': module})
