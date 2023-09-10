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
