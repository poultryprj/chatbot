# chatbot_app/models.py
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)  # Booking, Deposit, Loan
    weight_in_gms = models.IntegerField(null=True)
    transaction_details = models.TextField(null=True)
    status = models.CharField(max_length=10, default='Pending')  # Pending, Completed
