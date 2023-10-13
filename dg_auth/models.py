from django.db import models
from dg_user.models import UserModel

# Create your models here.

class AuthModel(models.Model):
    # id = models.BigAutoField(primary_key=True)
    token_session = models.CharField(unique=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    platform = models.CharField(null=True)
    app = models.CharField(null=True)
    app_version = models.CharField(null=True)
    request_headers = models.CharField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = "dg_auth"
        ordering = ["-created_at"]