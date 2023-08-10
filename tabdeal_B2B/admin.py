from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'credit']

    def save_model(self, request, obj, form, change):
        obj.save()
        IncreaseCredit.objects.create(seller=obj, amount=obj.credit)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'phone_number', 'amount', 'timestamp']


@admin.register(IncreaseCredit)
class IncreaseCreditAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'amount', 'timestamp']
