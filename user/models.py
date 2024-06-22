from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='users', on_delete=models.CASCADE)     
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2) 
    account_no = models.IntegerField(unique=True)
    def __str__(self):
        return str(self.account_no)
    
class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length= 100)    
    country = models.CharField(max_length=100)
    def __str__(self):
        return str(self.user.email)
    