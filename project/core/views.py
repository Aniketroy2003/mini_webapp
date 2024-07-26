from django.shortcuts import render, redirect,get_object_or_404
from .models import Tasks
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, TaskForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth import login

# Create your views here.

# signup
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    task = Tasks.objects.filter(user=request.user)
    return render(request, 'profile.html', {'task': task})

@login_required
def home(request):
    user = request.user
    task = Tasks.objects.all()
    query = request.GET.get('q', '')
    if query:
        task = Tasks.objects.filter(user=user, title__icontains=query)

    return render(request, 'home.html',{'task':task, 'user':user, 'query': query})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    todo = get_object_or_404(Tasks, id=task_id, user=request.user)
    todo.delete()
    return redirect('home')


@login_required
def edit_task(request, task_id):
    todo = get_object_or_404(Tasks, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST,request.FILES, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=todo)
    return render(request, 'edit_task.html', {'form': form, 'todo': todo})