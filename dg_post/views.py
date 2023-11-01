from dg_post.models import PostModel
from dg_post.serializer import PostSerializerAll
from dg_media.models import MediaModel

# Create your views here.
class Post():
    def get(pk):
        try:
            return PostModel.objects.get(pk=pk)
        except:
            return None

    def all():
        try:
            return PostModel.objects.all()
        except:
            return None
        
    def media(pk):
        try:
            return MediaModel.objects.filter(model_id=pk, deleted_at=None)
        except:
            return None

    def create(description, user):
        data = {
            "description": description,
            'user': user.pk
        }
        print(f"User id: {data}")
        try:
            serializer = PostSerializerAll(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Response
            response = Response()
            response.error = False
            response.data = serializer.data
            response.status_text = "CREATED"
            return response
        except Exception as e:
            # Response
            response = Response()
            response.error = True
            response.error_text = e.args
            response.data = None
            response.status_text = "NOT CREATED"
            return response

class Response():
    def __init__(self) -> None:
        self.error = False
        self.error_text = ""
        self.status_text = ""
        self.data = None