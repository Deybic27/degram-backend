from django.urls import path
from dg_api.views import PostApiWeb, userPostsApiWeb

urlpatterns_dg_api = [
    path('v1/post', PostApiWeb.as_view()),
    path('v1/users/profile/post', userPostsApiWeb.as_view()),
]