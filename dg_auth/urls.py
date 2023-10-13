from django.urls import path
from dg_auth.views import UserAuthApiWebRegister, UserAuthApiWebLogin, UserAuthApiWebLogout

urlpatterns_dg_auth = [
    path('v1/auth/register', UserAuthApiWebRegister.as_view()),
    path('v1/auth/login', UserAuthApiWebLogin.as_view()),
    path('v1/auth/logout', UserAuthApiWebLogout.as_view())
]