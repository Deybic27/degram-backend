from django.urls import path
from dg_user.views import UserApiWeb, UserApiWebDetail

urlpatterns_dg_user = [
    path('v1/users', UserApiWeb.as_view()),
    path('v1/users/<int:id>', UserApiWebDetail.as_view()),
]