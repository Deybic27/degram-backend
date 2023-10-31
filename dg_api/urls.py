from django.urls import path
from dg_api.views import PostApiWeb

urlpatterns_dg_api = [
    path('v1/post', PostApiWeb.as_view()),
]