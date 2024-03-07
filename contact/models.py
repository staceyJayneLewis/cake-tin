from django.db import models


class Contact(models.Model):
    name = models.CharField(
        max_length=254, null=False, blank=False)
    email = models.EmailField(
        max_length=254, null=False, blank=False)
    contact_number = models.CharField(
        max_length=25, null=True, blank=True)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name
