from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Todo


# SIGN UP
def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
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
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('todo')

    return render(request, 'login.html')


# LOGOUT
def log_out(request):
    logout(request)
    return redirect('login')


# TODO LIST + CREATE
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
def delete_todo(request, todo_id):
    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )

    todo.delete()

    return redirect('todo')


# COMPLETE / UNCOMPLETE
def toggle_todo(request, todo_id):
    todo = get_object_or_404(
        Todo,
        id=todo_id,
        user=request.user
    )

    todo.completed = not todo.completed
    todo.save()

    return redirect('todo')