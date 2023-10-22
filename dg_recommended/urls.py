from django.urls import path
from dg_recommended.views import UserRecommendedApiWeb

urlpatterns_dg_recommended = [
    path('v1/recommended/users', UserRecommendedApiWeb.as_view()),
]