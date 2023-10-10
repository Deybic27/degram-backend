from rest_framework.serializers import ModelSerializer
from dg_user.models import UserModel

class UserSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'fullname', 'username', 'phone', "email"]
        # fields = '__all__'
        
class UserSerializerAll(ModelSerializer):
    class Meta:
        model = UserModel
        # fields = ['id', 'user', 'phone', "email"]
        fields = '__all__'

class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'user', 'password']
        # fields = '__all__'