from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Todo

from django.utils import timezone
from datetime import datetime
from django.contrib import messages


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ✅ check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "signup.html")

        # ✅ create user safely
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created! Please login.")
        return redirect("login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("todo")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")



def todo_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    # ✅ get selected date or today
    selected_date = request.GET.get("date")
    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except:
            selected_date_obj = timezone.now().date()
    else:
        selected_date_obj = timezone.now().date()

    # ✅ add task
    if request.method == "POST":
        title = request.POST.get("title")
        task_date = request.POST.get("task_date")

        if title:
            if task_date:
                task_date_obj = datetime.strptime(task_date, "%Y-%m-%d").date()
            else:
                task_date_obj = timezone.now().date()

            Todo.objects.create(
                user=request.user,
                title=title,
                task_date=task_date_obj
            )
            return redirect(f"/todo/?date={task_date_obj}")

    # ✅ filter todos by date
    todos = Todo.objects.filter(
        user=request.user,
        task_date=selected_date_obj
    ).order_by("-created")

    context = {
        "todos": todos,
        "selected_date": selected_date_obj,
    }
    return render(request, "todo.html", context)


def delete_todo(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect("todo")
