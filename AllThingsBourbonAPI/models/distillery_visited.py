from django.db import models
from django.contrib.auth.models import User

class DistilleryVisited(models.Model):

    distillery_enthusiast = models.ForeignKey("BourbonUser", null=True, blank=True, on_delete=models.CASCADE, related_name='distillery_visited' )
    distillery = models.ForeignKey("Distillery", null=True, blank=True, on_delete=models.CASCADE, related_name='enthusiasts' )
    comments = models.CharField(max_length=500)
    rating = models.IntegerField(null=True, blank=True)

    @property 
    def is_distillery_enthusiast(self):
        return self.__distillery_enthusiast

    @is_distillery_enthusiast.setter
    def is_distillery_enthusiast(self, value):
        self.__distillery_enthusiast = value