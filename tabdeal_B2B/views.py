from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Seller, Transaction


@csrf_exempt
@api_view(['POST'])
@transaction.atomic
def increase_credits(request, seller_id):
    seller = Seller.objects.select_for_update().get(pk=seller_id)
    amount = float(request.data.get('amount', 0))
    if amount <= 0:
        return Response({'message': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

    seller.credits += amount
    seller.save()
    return Response({'message': f'Credits increased successfully in amount of {amount}'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@transaction.atomic
def transfer_credits(request, seller_id):
    seller = Seller.objects.select_for_update().get(pk=seller_id)
    phone_number = request.data.get('phone_number')
    amount = float(request.data.get('amount', 0))

    if amount <= 0 or amount > seller.credits:
        return Response({'message': 'Invalid amount or insufficient credits'}, status=status.HTTP_400_BAD_REQUEST)

    seller.credits -= amount
    seller.save()

    Transaction.objects.create(seller=seller, phone_number=phone_number, amount=amount)
    return Response({'message': f'Credits transferred successfully to {phone_number}'})


@csrf_exempt
@api_view(['POST'])
@transaction.atomic
def make_sellers(request):
    seller_name = request.data.get('name')
    if not seller_name:
        return Response({'message': 'Invalid seller name'}, status=status.HTTP_400_BAD_REQUEST)

    existing_seller = Seller.objects.filter(name=seller_name).first()
    if existing_seller:
        return Response({'message': 'Seller with the same name already exists'}, status=status.HTTP_400_BAD_REQUEST)

    Seller.objects.create(name=seller_name)
    return Response({'message': f'Seller {seller_name} created successfully'})
