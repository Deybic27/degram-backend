from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel, user_directory_path
from dg_user.serializer import UserInfoSummarySerializer
from dg_auth.views import validateSession

# Create your views here.
class UserRecommendedApiWeb(APIView):
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
        
        # Recommended
        listRecommended = UserModel.objects.all()[:7]
        serializer = UserInfoSummarySerializer(listRecommended, many=True)
        
        response.status=status.HTTP_200_OK
        response.data=serializer.data
        return  response