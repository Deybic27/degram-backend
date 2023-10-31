from django.urls import path
from dg_media.views import MediaUserApiWebUpload

urlpatterns_dg_media = [
    path('v1/medias/user/upload', MediaUserApiWebUpload.as_view()),
    # path('v1/medias/post/upload', MediaPostApiWebUpload.as_view()),
]