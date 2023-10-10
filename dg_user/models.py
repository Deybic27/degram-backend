from django.db import models

# Create your models here.

class UserModel(models.Model):
    # id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True,max_length=15)
    fullname = models.CharField(max_length=255)
    phone = models.BigIntegerField(unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=255)
    image = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = "user"
        ordering = ["-created_at"]