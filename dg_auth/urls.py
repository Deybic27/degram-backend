from django.urls import path
from dg_auth.views import UserAuthRegister, UserAuthLogin

urlpatterns_dg_auth = [
    path('v1/auth/register', UserAuthRegister.as_view()),
    path('v1/auth/login', UserAuthLogin.as_view())
]