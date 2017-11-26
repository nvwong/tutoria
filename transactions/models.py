from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wallet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=1)

    def __str__(self):
        return str(self.owner.username)

class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=1)
    timestamp = models.DateTimeField()
    def __str__(self):
        return str(self.amount)
