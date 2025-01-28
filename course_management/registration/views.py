from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserForm

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect("home")  # Redirect to home or dashboard
    else:
        form = CustomUserForm()
    return render(request, "register.html", {"form": form})


# Create your views here.
