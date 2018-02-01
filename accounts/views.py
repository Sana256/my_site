from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib import messages

User = get_user_model()
from accounts.forms import SignupForm
from accounts.tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account_activation_email.html', {'user': user, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(), 'token': account_activation_token.make_token(user)})
            user.email_user(subject, message)
            messages.success(request, "Check your email, we've sent you a link you can use to sign up.")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "User created")
        return redirect('/')
    else:
        messages.error(request, "Invalid user")
        return redirect('/')
