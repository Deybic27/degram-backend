from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel
from dg_media.models import MediaModel
from dg_post.models import PostModel
from dg_post.serializer import PostSerializerAll
from dg_media.serializer import MediaSerializerAll
from django.core.files.storage import FileSystemStorage
from dg_auth.views import validateSession
from dg_post.views import Post
from dg_user.views import User
from dg_media.views import Media
import time
import os

# Create your views here.
class PostApiWeb(APIView):    
    def post(self, request):

        # Response
        response = Response()
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        
        try:
            auth_token = request.COOKIES["dg_token_auth"]
            user_id = request.COOKIES["dg_user_id"]
        except Exception as e:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        
        # Session validate
        isLogued = validateSession(token=auth_token, user_id=user_id)
        if(isLogued == False):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        
        user = User.get(pk=user_id)
        if(user == None):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        
        
        image = request.FILES.get("image")
        description = request.POST.get("description")
        image_format = request.POST.get("image_format")
        print("HEREEE", image_format)
        # Post create
        post = Post.create(description=description, user=user)
        if(post.error == True):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response
        
        print("*************** POST CREATED ***************")
        print(f"POST {post.data}")
        print(f"USER {user.pk} -> {user.fullname}")
        print("*************** THE END POST CREATED ***************")
        
        # Media create
        media = Media.create(model_name="POST", model_id=post.data['id'], image=image, image_format=image_format)
        print("*************** MEDIA CREATED ***************")
        print(f"MEDIA {media.data}")
        print("*************** THE END MEDIA CREATED ***************")

        response.status_code = status.HTTP_201_CREATED
        return response