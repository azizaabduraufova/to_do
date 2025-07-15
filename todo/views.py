from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404


# Create your views here.

def home(request):
    return render(request, 'todo/home.html')



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')  # Change to your tasks view
    else:
        form = RegisterForm()
    return render(request, 'todo/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def task_list(request):
    tasks = Task.objects.all()  # or filter by user later
    return render(request, 'todo/task_list.html', {'tasks': tasks})

from .forms import TaskForm

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # If you want to assign the task to the current user later, do:
            # task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id) #, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'todo/delete_task.html', {'task': task})

from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id,) #user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


