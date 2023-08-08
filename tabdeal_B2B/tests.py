import json
import unittest

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Seller, Transaction

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Seller, Transaction


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_sellers_and_transactions(self):
        # Create two sellers
        response = self.client.post('/make_sellers/', {'name': 'Seller1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Seller.objects.count(), 1)

        response = self.client.post('/make_sellers/', {'name': 'Seller2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Seller.objects.count(), 2)

        seller1 = Seller.objects.get(name='Seller1')
        seller2 = Seller.objects.get(name='Seller2')

        # Increase credits for each seller
        response = self.client.post(f'/increase_credits/{seller1.id}/', {'amount': 60.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(f'/increase_credits/{seller2.id}/', {'amount': 140.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        seller1.refresh_from_db()
        seller2.refresh_from_db()

        self.assertEqual(seller1.credits, 60.0)
        self.assertEqual(seller2.credits, 140.0)

        response = self.client.post(f'/increase_credits/{seller1.id}/', {'amount': 40.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(f'/increase_credits/{seller2.id}/', {'amount': 60.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        seller1.refresh_from_db()
        seller2.refresh_from_db()

        self.assertEqual(seller1.credits, 100.0)
        self.assertEqual(seller2.credits, 200.0)
        # Perform transfers for each seller
        handle_1 = seller1.credits
        handle_2 = seller2.credits
        for i in range(10):
            amount = 1 * (i + 1)
            response = self.client.post(f'/transfer_credits/{seller1.id}/',
                                        {'phone_number': '123456789', 'amount': amount})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.client.post(f'/transfer_credits/{seller2.id}/',
                                        {'phone_number': '987654321', 'amount': amount})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            seller1.refresh_from_db()
            seller2.refresh_from_db()
            self.assertEqual(seller1.credits, handle_1 - amount)
            self.assertEqual(seller2.credits, handle_2 - amount)
            handle_1 = seller1.credits
            handle_2 = seller2.credits
            transactions_count = Transaction.objects.count()
            self.assertEqual(transactions_count, (i + 1) * 2)

        # Check the final credits and transactions
        self.assertEqual(seller1.credits, 100.0 - 55.0)
        self.assertEqual(seller2.credits, 200.0 - 55.0)
        self.assertEqual(Transaction.objects.count(), 20)


if __name__ == '__main__':
    unittest.main()
