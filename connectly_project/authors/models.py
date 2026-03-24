from django.db import models
from django.conf import settings

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name