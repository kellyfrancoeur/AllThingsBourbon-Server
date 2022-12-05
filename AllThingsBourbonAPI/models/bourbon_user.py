from django.db import models
from django.contrib.auth.models import User

class BourbonUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'