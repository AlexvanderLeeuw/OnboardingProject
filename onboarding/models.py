from django.db import models
from django.contrib.auth.models import User
from onboarding.choice_lists import CURRENCY_CHOICES

class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class Income(models.Model):
    source = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Expense(models.Model):
    source = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
