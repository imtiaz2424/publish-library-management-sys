from django.db import models
from user.models import UserAccount
from posts.models import Post
from .constants import TRANSACTION_TYPE

# Create your models here.


class Transaction(models.Model):
    users = models.ForeignKey(UserAccount, related_name = 'transactions', on_delete = models.CASCADE)    
    amount = models.DecimalField(decimal_places=2, max_digits = 10)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 10)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField(Post, related_name='posts')
    
    class Meta:
        ordering = ['timestamp'] 