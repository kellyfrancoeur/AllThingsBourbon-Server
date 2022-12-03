from django.db import models
from django.contrib.auth.models import User


class BourbonDescriptor(models.Model):

    bourbon_tried = models.ForeignKey("BourbonTried", null=True, blank=True, on_delete=models.CASCADE)
    descriptor = models.ForeignKey("Descriptor", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.descriptor.label