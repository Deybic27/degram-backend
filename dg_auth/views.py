from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel
from dg_user.serializer import UserSerializer, UserSerializerAll
import argon2, binascii
import base64
import datetime
import time
import hashlib

# Create your views here.

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

class UserAuthRegister(APIView):
    def post(self, request):
        pwd = base64.b64decode(request.POST["password"])
        try:
            email = request.POST["email"]
        except Exception:
            email = None
        try:
            phone = request.POST["phone"]
        except Exception:
            phone = None
            
        data = {
            "username": request.POST["username"],
            "fullname": request.POST["fullname"],
            "phone": phone,
            "email": email,
            "password": createHashPassword(pwd)
        }
        # Save
        serializer = UserSerializerAll(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        id = serializer.data["id"]
        id_bytes = str(id).encode("utf-8")
        id_base64 = base64.b64encode(id_bytes)
        now = f"{int(time.time())}:{id_base64}"
        token_bytes = now.encode('utf-8')
        token = hashlib.sha256(token_bytes).hexdigest()
        # Response
        response = Response()
        response.status_code = status.HTTP_201_CREATED
        # response["Dg-Auth-Token"] = token
        # response["Dg-User-Id"] = id
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        response.set_cookie(key="dg_token_auth", value=token, max_age=7776000, secure=True, samesite="None")
        response.set_cookie(key="dg_user_id", value=id, max_age=7776000, secure=True, samesite="None")
        
        return response
    
class UserAuthLogin(APIView):
    def get_by_username(self, username):
        try:
            return UserModel.objects.get(username=username)
        except:
            return None

    def post(self, request):
        username = request.POST['username']
        password = base64.b64decode(request.POST['password'])
        user = self.get_by_username(username)
        if (user == None):
            return Response(status=status.HTTP_403_FORBIDDEN, data="INVALID_USER")
        validPassword = validateHashPassword(user.password, password)
        if (validPassword == False):
            return Response(status=status.HTTP_403_FORBIDDEN, data="INVALID_PASSWORD")
        
        id = user.id
        id_bytes = str(id).encode("utf-8")
        id_base64 = base64.b64encode(id_bytes)
        now = f"{int(time.time())}:{id_base64}"
        token_bytes = now.encode('utf-8')
        token = hashlib.sha256(token_bytes).hexdigest()
        # Return Response
        response = Response()
        response.status_code = status.HTTP_202_ACCEPTED
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        response.set_cookie(key="dg_token_auth", value=token, max_age=7776000, secure=True, samesite="None")
        response.set_cookie(key="dg_user_id", value=id, max_age=7776000, secure=True, samesite="None")
        return response