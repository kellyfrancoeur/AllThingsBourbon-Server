from django.db import models
from django.contrib.auth.models import User

class Descriptor(models.Model):

    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label