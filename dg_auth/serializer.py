from rest_framework.serializers import ModelSerializer
from dg_auth.models import AuthModel

class AuthSerializerAll(ModelSerializer):
    class Meta:
        model = AuthModel
        fields = '__all__'
        # fields =  ["id","token_session","user_id","expires_at","created_at","updated_at","deleted_at"]