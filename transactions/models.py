from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=1)
    timestamp = models.DateTimeField()
    def __str__(self):
        return str(self.amount)
