from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel, user_directory_path
from dg_user.serializer import UserInfoSerializer, UserInfoSummarySerializer
from django.core.files.storage import FileSystemStorage
from dg_auth.views import validateSession
import time
import os

# Create your views here.

class UserApiWeb(APIView):
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

        # Validate session
        isLogued = validateSession(token=auth_token, user_id=user_id)
        if(isLogued == False):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        serializer = UserInfoSummarySerializer(UserModel.objects.all(), many=True)
        
        response.status=status.HTTP_200_OK
        response.data=serializer.data
        return  response
    
class UserApiWebInfo(APIView):
    def get_object(self, pk):
        try:
            return UserModel.objects.get(pk=pk)
        except:
            return None
    
    def get(self, request):
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
            
        user = self.get_object(user_id)
        serializer = UserInfoSerializer(user)
        response.data = serializer.data
        response.status_code = status.HTTP_200_OK
        
        print(f"************* GET USER DATA **************")
        print(f"{serializer.data}")
        print(f"************* THE END GET USER DATA **************")
    
        return response
    
    def post(self, request):
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
        
        now = time.time()
        nowGmt = time.gmtime(now)
        nowFormat = time.strftime("%Y-%m-%d %H:%M:%S", nowGmt)
        
        user = self.get_object(user_id)
        user.fullname = request.POST["fullname"]
        user.link = request.POST["link"]
        user.link_text = request.POST["link_text"]
        user.description = request.POST["description"]
        user.updated_at = nowFormat
        user.save()
        
        # Response
        response.status_code = status.HTTP_200_OK
        return response