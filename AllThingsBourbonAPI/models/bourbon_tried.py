from django.db import models
from django.contrib.auth.models import User

class BourbonTried(models.Model):

    bourbon_enthusiast = models.ForeignKey("BourbonUser", null=True, blank=True, on_delete=models.CASCADE, related_name='bourbons_tried' )
    bourbon = models.ForeignKey("Bourbon", null=True, blank=True, on_delete=models.CASCADE, related_name='enthusiasts')
    comments = models.CharField(max_length=500)
    rating = models.IntegerField(null=True, blank=True)
    descriptors = models.ManyToManyField("Descriptor", through = "BourbonDescriptor")

    @property 
    def is_bourbon_enthusiast(self):
        return self.__bourbon_enthusiast

    @is_bourbon_enthusiast.setter
    def is_bourbon_enthusiast(self, value):
        self.__bourbon_enthusiast = value
