from django.db import models

# Create your models here.
def user_directory_path(user, filename): 
  
    # file will be uploaded to MEDIA_ROOT / images/users/<id>/<filename> 
    return 'images/users/{0}/{1}'.format(user.id, filename) 

class UserModel(models.Model):
    # id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True,max_length=15)
    fullname = models.CharField(max_length=255)
    phone = models.BigIntegerField(unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=user_directory_path)
    description = models.CharField(null=True)
    link = models.CharField(null=True)
    link_text = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = "dg_user"
        ordering = ["-created_at"]