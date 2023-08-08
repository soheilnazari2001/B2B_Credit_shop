from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'credits']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'phone_number', 'amount', 'timestamp']
