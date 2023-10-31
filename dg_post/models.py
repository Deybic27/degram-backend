from django.db import models
from dg_user.models import UserModel

# Create your models here.
class PostModel(models.Model):
    STATUS = [
        (0, "draft"),
        (1, "published"),
        (2, "only_for_me"),
    ]
    description = models.CharField(blank=True)
    status = models.SmallIntegerField(choices=STATUS, default=1)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "dg_post"
        ordering = ["-created_at"]
        