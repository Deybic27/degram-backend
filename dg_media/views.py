from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel
from dg_media.models import MediaModel
from dg_post.models import PostModel
from dg_post.serializer import PostSerializerAll
from dg_user.serializer import UserInfoSerializer
from dg_media.serializer import MediaSerializerAll
from django.core.files.storage import FileSystemStorage
from dg_auth.views import validateSession
import time
import os

# Create your views here.
class Media():        
    def get(self, pk):
        try:
            return MediaModel.objects.get(pk=pk)
        except:
            return None
    
    def create(model_name, model_id, image, image_format):
        CONTENT_TYPES_ACCEPTED = {
            "image/jpeg": "jpg",
            "image/png": "png"
        }
        
        try:
            CONTENT_TYPES_ACCEPTED[image.content_type]
        except Exception as e:
            # Response
            response = Response()
            response.error = True
            response.data = {
                "TYPES_ACCEPTED": CONTENT_TYPES_ACCEPTED,
                "TYPES_NOT_ACCEPTED": e.args
            }
            response.status_text = "TYPES_NOT_ACCEPTED"
            return response
        
        IMAGE_FORMATS = {
            "1_1": 0,
            "4_5": 1,
            "16_9": 2,
        }
        try:
            IMAGE_FORMATS[image_format]
        except Exception as e:
            image_format = "1_1"

        now = time.time()
        nowGmt = time.gmtime(now)
        nowFormat = time.strftime("%Y-%m-%d %H:%M:%S", nowGmt)

        folder = os.path.join(model_name.lower(), f"{model_id}")
        newName = f"{folder}/{now}.{CONTENT_TYPES_ACCEPTED[image.content_type]}"
        
        # Save file
        pathSaved = FileSystemStorage().save(newName, image)

        # Create media
        media = MediaModel.objects.create(
            model_type=model_name,
            model_id=model_id,
            path=pathSaved,
            title=image.name,
            format=IMAGE_FORMATS[image_format]
        )
        mediaSerializer = MediaSerializerAll(media)
        
        print(f"************* USER IMAGE UPDATED **************")
        print(f"Model Id: {model_id}")
        print(f"{mediaSerializer.data['id']}: {mediaSerializer.data['model_type']}")
        print(f"Image: {pathSaved}")
        print(f"************* THE END USER IMAGE UPDATED **************")
        
        # Response
        response = Response()
        response.error = False
        response.data = mediaSerializer.data
        response.status_text = "CREATED"
        return response

class MediaUserApiWebUpload(APIView):
    def get_object(self, pk):
        try:
            return UserModel.objects.get(pk=pk)
        except:
            return None
    
    def post(self,request):
        auth_token = request.COOKIES["dg_token_auth"]
        user_id = request.COOKIES["dg_user_id"]
        
        # Response
        response = Response()
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        # Validate session
        isLogued = validateSession(token=auth_token, user_id=user_id)
        if(isLogued == False):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        
        CONTENT_TYPES_ACCEPTED = {
            "image/jpeg": "jpg",
            "image/png": "png"
        }
        image = request.FILES.get('image')
        
        try:
            CONTENT_TYPES_ACCEPTED[image.content_type]
        except Exception as e:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            response.data = [{"TYPES_ACCEPTED": CONTENT_TYPES_ACCEPTED},{"TYPES_NOT_ACCEPTED": e.args}]
            return response

        # Read user
        user = self.get_object(user_id)
        
        now = time.time()
        nowGmt = time.gmtime(now)
        nowFormat = time.strftime("%Y-%m-%d %H:%M:%S", nowGmt)
        
        folder = os.path.join("users", f"{user.id}")
        newName = f"{folder}/{user.username}_{now}.{CONTENT_TYPES_ACCEPTED[image.content_type]}"
        
        if (FileSystemStorage().exists(folder)):
            print(f"************* EXISTS FILE **************")
            directories, files = FileSystemStorage().listdir(folder)
            for file in files:
                print(f"Files: {file}")
                FileSystemStorage().delete(f"{folder}/{file}")
            print(f"Exist: {newName}")
            print(f"************* THE END EXISTS FILE **************")
        
        # Save file
        pathSaved = FileSystemStorage().save(newName, image)
        
        # Insert path
        user.image = pathSaved
        user.updated_at = nowFormat
        user.save()
        serializer = UserInfoSerializer(user)
        print(f"************* USER IMAGE UPDATED **************")
        print(f"{user.username}: {user.image}")
        print(f"Image: {pathSaved}")
        print(f"************* THE END USER IMAGE UPDATED **************")
        response.data = serializer.data["image"]
        response.status_code = status.HTTP_200_OK
        return response
    
# class MediaPostApiWebUpload(APIView):
#     def get_user(self, pk):
#         try:
#             return UserModel.objects.get(pk=pk)
#         except:
#             return None
        
#     def get_media(self, pk):
#         try:
#             return MediaModel.objects.get(pk=pk)
#         except:
#             return None
        
#     def get_post(self, pk):
#         try:
#             return PostModel.objects.get(pk=pk)
#         except:
#             return None
    
#     def post(self,request):
#         # Response
#         response = Response()
#         response["Access-Control-Allow-Credentials"] = "true"
#         response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        
#         try:
#             auth_token = request.COOKIES["dg_token_auth"]
#             user_id = request.COOKIES["dg_user_id"]
#         except Exception as e:
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return response
        
#         # Validate session
#         isLogued = validateSession(token=auth_token, user_id=user_id)
#         if(isLogued == False):
#             response.status_code = status.HTTP_401_UNAUTHORIZED
#             return response
        
#         CONTENT_TYPES_ACCEPTED = {
#             "image/jpeg": "jpg",
#             "image/png": "png"
#         }
#         image = request.FILES.get('image')
        
#         try:
#             CONTENT_TYPES_ACCEPTED[image.content_type]
#         except Exception as e:
#             response.status_code = status.HTTP_406_NOT_ACCEPTABLE
#             response.data = [{"TYPES_ACCEPTED": CONTENT_TYPES_ACCEPTED},{"TYPES_NOT_ACCEPTED": e.args}]
#             return response

#         # Create post
#         user = self.get_user(user_id)
#         data = {
#             "description": "",
#             "status": 0,
#             "user": user.pk
#         }
#         postSerializer = PostSerializerAll(data=data)
#         postSerializer.is_valid(raise_exception=True)
#         postSerializer.save()

#         now = time.time()
#         nowGmt = time.gmtime(now)
#         nowFormat = time.strftime("%Y-%m-%d %H:%M:%S", nowGmt)

#         folder = os.path.join("posts", f"{model_id}")
#         newName = f"{folder}/{now}.{CONTENT_TYPES_ACCEPTED[image.content_type]}"
        
#         # Save file
#         pathSaved = FileSystemStorage().save(newName, image)
#         print("*******--- ", type(pathSaved))

#         # Create media
#         data = {
#             "model_type": "media",
#             "model_id": model_id,
#             "path": pathSaved,
#             "title": image.name
#         }
#         media = MediaModel.objects.create(
#             model_type="MediaModel",
#             model_id=model_id,
#             path=pathSaved,
#             title=image.name
#         )
#         mediaSerializer = MediaSerializerAll(media)
        
        
#         print(f"************* USER IMAGE UPDATED **************")
#         print(f"{model_id}: {postSerializer.data['description']}")
#         print(f"{mediaSerializer.data['id']}: {mediaSerializer.data['model_type']}")
#         print(f"Image: {pathSaved}")
#         print(f"************* THE END USER IMAGE UPDATED **************")
#         response.data = mediaSerializer.data["path"]
#         response.status_code = status.HTTP_200_OK
#         return response

class Response():
    def __init__(self) -> None:
        self.error = False
        self.error_text = ""
        self.status_text = ""
        self.data = None