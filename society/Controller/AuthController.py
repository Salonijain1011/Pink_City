from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username, password=password)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
    return render(request, "register.html")


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")
from django.contrib.auth import logout
from django.shortcuts import redirect

@never_cache
def user_logout(request):
    # Log the user out
    logout(request)

    # Clear session cookies (optional, since they will usually be cleared upon logout)
    response = redirect('/login/')  # Redirect to the login page

    # Clear cookies explicitly, if necessary
    response.delete_cookie('sessionid')  # Adjust if your cookie name is different
    response.delete_cookie('csrftoken')   # Clear CSRF cookie if needed

    return response
