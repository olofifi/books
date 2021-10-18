from django.core import serializers
from django.db import models

# Create your models here.
class BookModel(models.Model):
    data = models.JSONField(default=None)

