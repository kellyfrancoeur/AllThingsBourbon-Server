from django.db import models
from django.contrib.auth.models import User

class CocktailTried(models.Model):

    cocktail_enthusiast = models.ForeignKey("BourbonUser", null=True, blank=True, on_delete=models.CASCADE, related_name='cocktails_tried' )
    cocktail = models.ForeignKey("Cocktail", null=True, blank=True, on_delete=models.CASCADE, related_name='enthusiasts')
    comments = models.CharField(max_length=500)
    rating = models.IntegerField(null=True, blank=True)

    @property 
    def is_cocktail_enthusiast(self):
        return self.__cocktail_enthusiast

    @is_cocktail_enthusiast.setter
    def is_cocktail_enthusiast(self, value):
        self.__cocktail_enthusiast = value
