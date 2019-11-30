from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import UpdateView

from HCI.forms import SignupForm
from HCI.utils.email_functions import send_email, account_activation_token


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email(request, user)
            return render(request, 'message.html', {
                'title': "Sign Up Successful",
                'message': "Thank you for signing up. An activation link is sent to your email. Please Activate your "
                           "account using that link",
            })
    else:
        form = SignupForm()
    return render(request, 'account/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'message.html', {
            'title': "Your Account is Activated",
            'message': 'Thank you for your email confirmation. Now you can login your account.',
        })
    else:
        return render(request, 'message.html', {
            'title': "Something went wrong",
            'message': 'Activation link is invalid!',
        })


class UserProfileView(UpdateView):
    model = User
    template_name = 'account/profile.html'
    success_url = reverse_lazy('profile')
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView2(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change.html'


def password_change_done_view(request):
    return render(request, 'message.html', {
        'title': "Password Changed",
        'message': 'Your password has been successfully changed!',
    })

