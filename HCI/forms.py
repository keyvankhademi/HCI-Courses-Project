from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import requests

from HCI_Course.settings import SETTINGS_JSON


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    def is_valid(self):
        response = self.data['g-recaptcha-response']
        key = SETTINGS_JSON['reCaptcha_key']

        r = requests.post(SETTINGS_JSON['reCaptcha_url'], {
            'secret': key,
            'response': response,
        })

        data = r.json()

        if not data['success']:
            self.add_error(None, 'reCaptcha should be validate')
            return False

        return super(SignupForm, self).is_valid()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
