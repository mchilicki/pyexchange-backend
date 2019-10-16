from django.db import models


# Create your models here.


class User(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=5000)
    money = models.IntegerField(default=0)


class Currency(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    unit = models.IntegerField(default=1)
    purchase_price = models.FloatField(default=0)
    sell_price = models.FloatField(default=0)


class UserCurrency(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)



