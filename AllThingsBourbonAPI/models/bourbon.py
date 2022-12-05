from django.db import models
from django.contrib.auth.models import User

class Bourbon(models.Model):

    name = models.CharField(max_length=100)
    proof = models.IntegerField(null=True, blank=True)
    aroma = models.CharField(max_length=500)
    taste = models.CharField(max_length=500)
    finish = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    made_in = models.CharField(max_length=75)
    link_to_buy = models.CharField(max_length=150)
    bourbon_img = models.CharField(max_length=500)
    type_of_bourbon = models.ForeignKey("BourbonType", null=True, blank=True, on_delete=models.CASCADE, related_name='bourbons')
    staff_member = models.ForeignKey("BourbonStaff", null=True, blank=True, on_delete=models.CASCADE, related_name='new_bourbon')
