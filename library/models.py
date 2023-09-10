from django.db import models

# Create your models here.
class Title(models.Model):
    name = models.CharField(max_length=256)
    bgg_id = models.IntegerField(null=True)
