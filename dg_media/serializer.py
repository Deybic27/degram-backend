from rest_framework.serializers import ModelSerializer
from dg_media.models import MediaModel

class MediaSerializerAll(ModelSerializer):
    class Meta:
        model = MediaModel
        # fields = ['id', 'user', 'phone', "email"]
        fields = '__all__'