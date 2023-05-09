from django.db import models

# Create your models here.

# todo: 
# add string representations using __str__

# Table of user 
class User(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    salt = models.CharField(max_length=30)
    balance = models.FloatField()
    currency_id = models.CharField(max_length=3)

    # def __str__(self):


# Table of Billing addresses
class Billing(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address_line_1 = models.CharField(max_length=30)
    address_line_2 = models.CharField(max_length=30, blank=True, null=True)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)

# table of transactions
class Transaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField()
    currency_id = models.CharField(max_length=3)
    fee = models.FloatField()
    confirmed = models.BooleanField(default=False)
    recipient_id = models.PositiveIntegerField()



