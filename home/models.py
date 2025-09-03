from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    guest_name = models.CharField(max_length=255, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    tran_id = models.CharField(max_length=100, unique=True)
    val_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    payment_info = models.JSONField(null=True,blank=True)  # stores full payment info as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tran_id} - {self.status}"