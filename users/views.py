from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm


# ==============================
# რეგისტრაცია
# ==============================
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'page_title': 'რეგისტრაცია'})


# ==============================
# პირადი გვერდი
# ==============================
@login_required
def profile(request):
    return render(request, 'users/profile.html', {'page_title': 'ჩემი გვერდი'})


# ==============================
# პროფილის განახლება
# ==============================
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form, 'page_title': 'პროფილის რედაქტირება'})


# ==============================
# Custom Logout
# ==============================
def custom_logout(request):
    logout(request)
    return redirect('home')
