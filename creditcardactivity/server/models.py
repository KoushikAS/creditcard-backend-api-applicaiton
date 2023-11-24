from django.db import models

class User(models.Model):
    userId = models.CharField(max_length=100, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    available_credit = models.DecimalField(max_digits=10, decimal_places=2)

class Pending_Transaction(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    txnId = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    initialTime = models.CharField(max_length=100)
    is_settled = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

class Settled_Transaction(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    txnId = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    finalTime = models.CharField(max_length=100)
    initialTime = models.CharField(max_length=100)