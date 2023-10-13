from django.urls import path
from dg_user.views import UserApiWeb, UserApiWebInfo

urlpatterns_dg_user = [
    path('v1/users', UserApiWeb.as_view()),
    path('v1/users/profile/info', UserApiWebInfo.as_view()),
]