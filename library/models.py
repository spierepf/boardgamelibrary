import uuid as uuid
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Title(models.Model):
    name = models.CharField(max_length=256)
    bgg_id = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bgg_id"], name="unique_bgg_id"
            )
        ]


class Copy(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["uuid"], name="unique_copy_uuid"
            )
        ]
