from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *


@csrf_exempt
@api_view(['POST'])
def increase_credits(request, seller_id):
    seller = Seller.objects.select_for_update().get(pk=seller_id)
    amount = float(request.data.get('amount', 0))
    try:
        seller.increase_credit(amount)
        return Response({'message': f'Credits increased successfully in amount of {amount}'}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'message': f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def transfer_credits(request, seller_id):
    seller = Seller.objects.select_for_update().get(pk=seller_id)
    phone_number = request.data.get('phone_number')
    amount = float(request.data.get('amount', 0))
    try:
        seller.transfer_credits(phone_number, amount)
        return Response({'message': f'Credits transferred successfully to {phone_number}'}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'message': f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def make_sellers(request):
    seller_name = request.data.get('name')
    credit = float(request.data.get('credit'))
    try:
        Seller.create_seller(seller_name, credit)
        return Response({'message': f'Seller {seller_name} created successfully and increased with {credit} credits'},
                        status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({'message': f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)
