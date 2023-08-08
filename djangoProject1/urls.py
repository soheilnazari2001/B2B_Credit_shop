from django.contrib import admin
from django.urls import path

from django.shortcuts import HttpResponse

from tabdeal_B2B import views
from tabdeal_B2B.views import *

urlpatterns = [
    path('increase_credits/<int:seller_id>/', views.increase_credits, name='increase_credits'),
    path('transfer_credits/<int:seller_id>/', views.transfer_credits, name='transfer_credits'),
    path('make_sellers/', views.make_sellers, name='make_sellers'),
    path('admin/', admin.site.urls),
]