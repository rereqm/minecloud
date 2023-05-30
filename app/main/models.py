from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from main.forms_utils import user_directory_path


class User(AbstractUser):
    logo_image = models.ImageField(upload_to=user_directory_path, default='default.svg')
    money = models.FloatField(default=0)


class Server(models.Model):
    name = models.CharField(max_length=15)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    plan = models.CharField(max_length=10)
    settings = models.JSONField(default=None)
    docker_id = models.CharField(max_length=64)
    remaining_days = models.IntegerField(default=0)
    status = models.CharField(default='stop', max_length=10)
    paid = models.BooleanField(default=False)
