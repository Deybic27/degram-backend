from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel
from dg_media.models import MediaModel
from dg_post.models import PostModel
from dg_post.serializer import PostInfoSerializer
from dg_media.serializer import MediaInfoSerializer
from dg_user.serializer import UserInfoBasicSerializer
from django.core.files.storage import FileSystemStorage
from dg_auth.views import validateSession
from dg_post.views import Post
from dg_user.views import User
from dg_media.views import Media
import time
import datetime
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
    
    def get(self, request):
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
        
        currentUser = User.get(pk=user_id)
        if(currentUser == None):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        
        posts = Post.all()
        listPost = []
        for post in posts:
            medias = Post.media(post.pk)
            for media in medias:

                postSerializer = PostInfoSerializer(post).data
                mediaSerializer = MediaInfoSerializer(media).data
                userSerializer = UserInfoBasicSerializer(post.user).data
                
                resp = {
                    "id": postSerializer['id'],
                    "description": postSerializer["description"],
                    "status": postSerializer["status"],
                    "status_text": post.get_status_display(),
                    "created_at": postSerializer["created_at"],
                    "time": "3d",
                    "user": userSerializer,
                    "media": {
                        "id": mediaSerializer["id"],
                        "path": mediaSerializer["path"],
                        "title": mediaSerializer["title"],
                        "format": mediaSerializer["format"],
                        "format_text": media.get_format_display(),
                    },
                }
                listPost.append(resp)
        
        response.data = listPost
        response.status_code = status.HTTP_200_OK
        return response

class userPostsApiWeb(APIView):
    def get(self, request):
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
        
        currentUser = User.get(pk=user_id)
        if(currentUser == None):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        
        posts = User.posts(pk=currentUser.pk)
        listPost = []
        for post in posts:
            medias = Post.media(post.pk)
            for media in medias:

                postSerializer = PostInfoSerializer(post).data
                mediaSerializer = MediaInfoSerializer(media).data
                resp = {
                    "id": postSerializer['id'],
                    "description": postSerializer["description"],
                    "status": postSerializer["status"],
                    "status_text": post.get_status_display(),
                    "created_at": postSerializer["created_at"],
                    "user": postSerializer["user"],
                    "media": {
                        "id": mediaSerializer["id"],
                        "path": mediaSerializer["path"],
                        "title": mediaSerializer["title"],
                        "format": mediaSerializer["format"],
                        "format_text": media.get_format_display(),
                    },
                }
                listPost.append(resp)
        
        response.data = listPost
        response.status_code = status.HTTP_200_OK
        return response