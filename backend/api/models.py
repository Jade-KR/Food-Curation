from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=2, null=True)
    # @property
    # def review_count(self):

    #     return self.
    review_count = models.IntegerField(default=0)
    

class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(max_length=10, null=True)
    longitude = models.FloatField(max_length=10, null=True)
    category = models.CharField(max_length=200, null=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_stores", blank=True)
    location = models.IntegerField()
    review_count = models.IntegerField(default=0)
    @property
    def category_list(self):
        return self.category.split("|") if self.category else []

    def __str__(self):
        return self.store_name


class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=126, null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.menu_name


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    content = models.TextField()
    reg_time = models.DateTimeField()

    def __str__(self):
        return self.content


class UserLikeStore(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 'api_store_like_users'


class StoreImage(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    url = models.TextField()