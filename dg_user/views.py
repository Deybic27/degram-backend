from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel
from dg_user.serializer import UserSerializer, UserSerializerAll
import argon2, binascii
import re

def createHashPassword(text):
    hash = argon2.hash_password_raw(
        time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32,
        password=b'password', salt=b'some salt', type=argon2.low_level.Type.ID)
    print("Argon2 raw hash:", binascii.hexlify(hash))
    argon2Hasher = argon2.PasswordHasher(
        time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
    hash = argon2Hasher.hash(text)
    return hash

def validateHashPassword(hash, text):
    # hash = "$argon2id$v=19$m=32768,t=16,p=2$cUolipL1iz81WcukKjOi6Q$MatHDbel8+4l4Mhfzw49Fzysb+klnKa8KwmFORUQjS4"
    # t = re.findall(r't=\d+', hash)[0].split("=")[1]
    # m = re.findall(r'm=\d+', hash)[0].split("=")[1]
    # p = re.findall(r'p=\d+', hash)[0].split("=")[1]
    # print(t, "T")
    # print(m, "M")
    # print(p, "P")
    argon2Hasher = argon2.PasswordHasher(
        time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
    try:
        argon2Hasher.verify(hash, text)
        return True
    except:
        return False

# Create your views here.

class UserApiWeb(APIView):
    def get(self, request):
        serializer = UserSerializerAll(UserModel.objects.all(), many=True)
        return  Response(status=status.HTTP_200_OK, data=serializer.data)
    
class UserApiWebDetail(APIView):
    def get_object(self, pk):
        try:
            return UserModel.objects.get(pk=pk)
        except:
            return None
    
    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        response = { 'delete': True}
        return Response(status=status.HTTP_200_OK, data=response)