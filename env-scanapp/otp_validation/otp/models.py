from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.db.models.fields.related import ForeignKey
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from jsonfield import JSONField
# Create your models here.


class User(AbstractUser):
    uid = models.CharField(max_length=100, unique=True, null=True)
    address = models.TextField(null=False)
    phone_number = models.IntegerField(unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.email


class ContactList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contacts = JSONField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
