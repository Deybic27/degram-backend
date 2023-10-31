from django.db import models

# Create your models here.
def user_directory_path(modelName, model, filename): 
  
    # file will be uploaded to MEDIA_ROOT / images/users/<id>/<filename> 
    return 'images/{0}/{1}/{2}'.format(modelName, model.id, filename) 

# Create your models here.
class MediaModel(models.Model):
    FORMATS = [
        (0, "1_1"),
        (1, "4_5"),
        (2, "16_9"),
    ]
    model_type = models.CharField()
    model_id = models.BigIntegerField()
    path = models.ImageField(null=True, upload_to=user_directory_path)
    title = models.CharField()
    format = models.SmallIntegerField(choices=FORMATS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = "dg_media"
        ordering = ["-created_at"]