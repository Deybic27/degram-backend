from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel
from dg_user.serializer import UserInfoSerializer
from django.core.files.storage import FileSystemStorage
from dg_auth.views import validateSession
import time
import os

# Create your views here.
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