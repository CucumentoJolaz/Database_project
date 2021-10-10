from django.contrib.auth.forms import AuthenticationForm

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = ""
        self.fields['password'].label = ""

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите логин',
               'id': 'login',
               }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'id': 'password',
            'required':'False',

        }
))
