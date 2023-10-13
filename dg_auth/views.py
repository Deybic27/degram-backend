from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from dg_user.models import UserModel
from dg_user.serializer import UserSerializer, UserSerializerAll
from dg_auth.models import AuthModel
from dg_auth.serializer import AuthSerializerAll
import argon2, binascii
import base64
import datetime
import time
import hashlib
import re

# Create your views here.

def createHashPassword(text):
    hash = argon2.hash_password_raw(
        time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32,
        password=b'password', salt=b'some salt', type=argon2.low_level.Type.ID)
    # print("Argon2 raw hash:", binascii.hexlify(hash))
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

def createSession(request, user_id):
    HEADERS = request.headers
    now = time.time()
    nowGmt = time.gmtime(now)
    nowFormat = time.strftime("%Y-%m-%d %H:%M:%S", nowGmt)
    try:
        platform = HEADERS['Sec-Ch-Ua-Platform'].replace('"', "")
    except Exception as e:
        platform = None
        print(f"\n****************** Except Platform ******************\n")
        print(f"Platform excep: {e} : {HEADERS}")
        print(f"\n****************** The End Except Platform ******************\n")
        
    try:
        appData = HEADERS['Sec-Ch-Ua']
        appDataSplit = appData.split(";")
        app = appDataSplit[0].replace('"', "")
        app_version = re.findall(r'\d+', appDataSplit[1])[0]
    except Exception as e:
        app = None
        app_version = None
        appData = None
        print(f"\n****************** Except Platform ******************\n")
        print(f"Platform excep: {e} : {HEADERS}")
        print(f"\n****************** The End Except Platform ******************\n")
    

    try:
        auths = AuthModel.objects.filter(user_id=user_id, platform=platform, app=app, app_version=app_version, deleted_at=None)
        
        for auth in auths:
            auth.deleted_at = nowFormat
            auth.updated_at = nowFormat
            auth.save()
    except Exception as e:
        auth = e
        print(f"\n****************** Except Auth Validate ******************\n")
        print(f"\nEXECP: {auth}\n")
        print(f"\n****************** The End Except Auth Validate ******************\n")
    
    id_bytes = str(user_id).encode("utf-8")
    id_base64 = base64.b64encode(id_bytes)
    token_text = f"{int(now)}:{id_base64}"
    token_bytes = token_text.encode('utf-8')
    token = hashlib.sha256(token_bytes).hexdigest()

    print(f"\n******* CREATE SESSION ******* \nTOKEN: {token}\nUSER_ID: {user_id}\nAPP DATA: {appData}\nAPP: {app}\nAPP_VERSION: {app_version}\nPLATFORM: {platform}\n******* THE END CREATE SESSION *******\n")
    expiresAtUnix = time.gmtime(now + 31556926)
    expiresAtFormat = time.strftime("%Y-%m-%d %H:%M:%S", expiresAtUnix)
    data = {
        "token_session": token,
        "user": user_id,
        "expires_at": expiresAtFormat,
        "platform": platform,
        "app": app,
        "app_version": app_version,
        "request_headers": str(HEADERS)
    }
    serializer = AuthSerializerAll(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return token

def validateSession(token, user_id):
    auths = AuthModel.objects.filter(user_id=user_id, token_session=token, deleted_at=None)
    auths_num = len(auths)
    print(f"************* IS LOGUED **************")
    print(f"{auths_num} sessiones activas")
    print(f"Token: {token}")
    print(f"User id: {user_id}")
    print(f"************* THE END IS LOGUED **************")
    if(auths_num > 0):
        return True
    return False

class UserAuthApiWebRegister(APIView):
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
        token = createSession(request=request, user_id=id)
        # Response
        response = Response()
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        response.set_cookie(key="dg_token_auth", value=token, max_age=31556926, secure=True, samesite="None")
        response.set_cookie(key="dg_user_id", value=id, max_age=31556926, secure=True, samesite="None")
        response.status_code = status.HTTP_201_CREATED
        
        return response
    
class UserAuthApiWebLogin(APIView):
    def get_by_username(self, username):
        try:
            return UserModel.objects.get(username=username)
        except:
            return None

    def post(self, request):
        username = request.POST['username']
        password = base64.b64decode(request.POST['password'])
        user = self.get_by_username(username)
        
        # Return Response
        response = Response()
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        if (user == None):
            response.status_code=status.HTTP_404_NOT_FOUND
            response.data = "INVALID_USER"
            return response
        validPassword = validateHashPassword(user.password, password)
        if (validPassword == False):
            response.status_code=status.HTTP_404_NOT_FOUND
            response.data = "INVALID_PASSWORD"
            return response
        
        id = user.id
        token = createSession(request=request, user_id=id)
        # Return Response
        response.set_cookie(key="dg_token_auth", value=token, max_age=31556926, secure=True, samesite="None")
        response.set_cookie(key="dg_user_id", value=id, max_age=31556926, secure=True, samesite="None")
        response.status_code = status.HTTP_202_ACCEPTED
        return response
    
class UserAuthApiWebLogout(APIView):
    def post(self, request):
        now = time.time()
        nowGmt = time.gmtime(now)
        nowFormat = time.strftime("%Y-%m-%d %H:%M:%S", nowGmt)
        auth_token = request.COOKIES["dg_token_auth"]
        user_id = request.COOKIES["dg_user_id"]
        
        auths = AuthModel.objects.filter(user_id=user_id, token_session=auth_token, deleted_at=None)
        for auth in auths:
            auth.deleted_at = nowFormat
            auth.updated_at = nowFormat
            auth.save()
        
        
        response = Response()
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:70"
        response.delete_cookie(key="dg_token_auth")
        response.delete_cookie(key="dg_user_id")
        response.status_code = status.HTTP_200_OK
        
        return response