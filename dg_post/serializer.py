from rest_framework.serializers import ModelSerializer
from dg_post.models import PostModel

class PostSerializerAll(ModelSerializer):
    class Meta:
        model = PostModel
        # fields = ['id', 'user', 'phone', "email"]
        fields = '__all__'
