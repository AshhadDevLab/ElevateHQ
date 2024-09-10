from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
    else:
        return render(request, "auth/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        # if User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=email).exists():
        #     return render(request, "auth/register.html")
        User.objects.create_user(username, email, password)
        return redirect("/")
    else:
        return render(request, "auth/register.html")