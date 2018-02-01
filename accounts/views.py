from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth import get_user_model

from accounts.forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
