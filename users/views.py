from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.tokens import default_token_generator


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


def form_valid(self, form):
    user = form.save(commit=False)
    user.is_active = False
    user.save()

    user_token = default_token_generator.make_token(user)

    send_mail(
        'Confirm your email',
        f'Please click the link to confirm your email: http://localhost:8000/confirm-email/{user.pk}/{user_token}/',
        'leriniaza17@gmail.com',
        [user.email],
    )

    return redirect('login')

def activate_user(request, user_id, token):
    user = User.objects.get(pk=user_id)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Your account has been activated. You can now log in.')
    else:
        return HttpResponse('Activation link is invalid!')


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
