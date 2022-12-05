from django.db import models
from django.contrib.auth.models import User

class Distillery(models.Model):

    name = models.CharField(max_length=150)
    location = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    link_to_site = models.CharField(max_length=500)
    distillery_img = models.CharField(max_length=500)
    staff_member = models.ForeignKey("BourbonStaff", null=True, blank=True, on_delete=models.CASCADE, related_name='new_distillery')