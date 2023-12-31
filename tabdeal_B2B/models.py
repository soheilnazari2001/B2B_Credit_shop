import threading
from decimal import Decimal

from django.db import models, transaction


class Seller(models.Model):
    name = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    lock = threading.Lock()

    def __str__(self):
        return f'{self.name} - {self.credit}'

    @classmethod
    def create_seller(cls, seller_name, first_credit):
        if not seller_name:
            raise ValueError('Invalid seller name')
        existing_seller = cls.objects.filter(name=seller_name).first()
        if existing_seller:
            raise ValueError('Seller with the same name already exists')
        with transaction.atomic():
            seller = cls.objects.create(name=seller_name, credit=first_credit)
            IncreaseCredit.objects.create(seller=seller, amount=first_credit)
            return seller

    def increase_credit(self, credit_amount):
        if credit_amount < 0:
            raise ValueError('Invalid amount')

        with transaction.atomic():
            self.refresh_from_db()
            self.lock.acquire()
            self.credit += Decimal(credit_amount)
            IncreaseCredit.objects.create(seller=self, amount=credit_amount)
            self.save()
            self.lock.release()

    def transfer_credits(self, phone_number, amount):
        if amount < 0:
            raise ValueError('Invalid amount')
        elif amount > self.credit:
            raise ValueError('Insufficient credits')
        with transaction.atomic():
            self.refresh_from_db()
            self.lock.acquire()
            self.credit -= amount
            self.save()
            Transaction.objects.create(seller=self, phone_number=phone_number, amount=amount)
            self.lock.release()


class Transaction(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='transactions')
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.seller.name} - {self.phone_number} - {self.amount} - {self.timestamp}'


class IncreaseCredit(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='increase_credits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.seller.name} - {self.amount} - {self.timestamp}'
