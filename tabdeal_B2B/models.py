from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=100)
    credits = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.name} - {self.credits}'


class Transaction(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.seller.name} - {self.phone_number} - {self.amount} - {self.timestamp}'
