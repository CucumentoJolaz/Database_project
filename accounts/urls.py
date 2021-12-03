from django.urls import path
from django.contrib.auth import views
from .views import SignUpView
from accounts import views as acc
from accounts.forms import UserLoginForm

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/',
    views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'),
]
