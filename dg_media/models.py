from django.db import models

# Create your models here.
class MediaModel(models.Model):
    model_type = models.CharField()
    model_id = models.BigIntegerField()
    path = models.CharField()
    title = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = "dg_media"
        ordering = ["-created_at"]