from django.db import models
from django.contrib.auth.models import User

class Cocktail(models.Model):

    name = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=500)
    how_to_make = models.CharField(max_length=1000)
    cocktail_img = models.CharField(max_length=500)
    type_of_cocktail = models.ForeignKey("CocktailType", null=True, blank=True, on_delete=models.CASCADE, related_name='cocktails')
    staff_member = models.ForeignKey("BourbonStaff", null=True, blank=True, on_delete=models.CASCADE, related_name='new_cocktail')