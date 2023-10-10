from django.db import models

# Create your models here.

class AuthModel(models.Model):
    # id = models.BigAutoField(primary_key=True)
    token_session = models.CharField(unique=True)
    user_id = models.IntegerField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = "auth"
        ordering = ["-created_at"]