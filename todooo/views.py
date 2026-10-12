from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo


# SIGN UP
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('todo')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            # This was the cause of the 500 error (IntegrityError)
            messages.error(request, 'This username is already taken.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('todo')

    return render(request, 'signup.html')


# LOGIN
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('todo')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# LOGOUT
def log_out(request):
    logout(request)
    return redirect('login')


# TODO LIST + CREATE
@login_required(login_url='login')
def to_do(request):
    if request.method == 'POST':
        title = request.POST['title']

        Todo.objects.create(
            title=title,
            user=request.user
        )

        return redirect('todo')

    todos = Todo.objects.filter(user=request.user)

    return render(request, 'todo.html', {'todos': todos})


# UPDATE
@login_required(login_url='login')
def update_todo(request, todo_id):
    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )

    if request.method == 'POST':
        todo.title = request.POST['title']
        todo.save()

        return redirect('todo')

    return render(request, 'update.html', {'todo': todo})


# DELETE
@login_required(login_url='login')
def delete_todo(request, todo_id):
    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )

    todo.delete()

    return redirect('todo')


# COMPLETE / UNCOMPLETE
@login_required(login_url='login')
def toggle_todo(request, todo_id):
    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )

    todo.completed = not todo.completed
    todo.save()

    return redirect('todo')