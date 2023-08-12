import threading
import unittest

from django.db.models import F

from .models import Seller, Transaction, IncreaseCredit
from rest_framework.test import APIClient
from .models import Seller, Transaction
from django.db import connections, transaction
from django.test import TestCase, override_settings
from decimal import Decimal
from rest_framework import status
from threading import local, Thread

db_connection = connections['default']


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def testSingleThreaded(self):
        response = self.client.post('/make_sellers/', {'name': 'Seller1', 'credit': 0.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Seller.objects.count(), 1)

        response = self.client.post('/make_sellers/', {'name': 'Seller2', 'credit': 0.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Seller.objects.count(), 2)

        seller1 = Seller.objects.get(name='Seller1')
        seller2 = Seller.objects.get(name='Seller2')

        credit_user1 = 100.00
        credit_user2 = 200.00
        for i in range(1000):
            if i % 100 == 0:
                response = self.client.post(f'/increase_credits/{seller1.id}/', {'amount': credit_user1})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(IncreaseCredit.objects.count(), 2 * (i // 100 + 1) + 1)
                seller1.refresh_from_db()
                self.assertEqual(seller1.credit, credit_user1 * (i // 100 + 1) - i)
                response = self.client.post(f'/increase_credits/{seller2.id}/', {'amount': credit_user2})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(IncreaseCredit.objects.count(), 2 * (i // 100 + 1) + 2)
                seller2.refresh_from_db()
                self.assertEqual(seller2.credit, credit_user2 * (i // 100 + 1) - 2 * i)
            response = self.client.post(f'/transfer_credits/{seller1.id}/',
                                        {'phone_number': '123456789', 'amount': 1.00})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self.client.post(f'/transfer_credits/{seller2.id}/',
                                        {'phone_number': '987654321', 'amount': 2.00})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            seller1.refresh_from_db()
            seller2.refresh_from_db()
            transactions_count = Transaction.objects.count()
            self.assertEqual(transactions_count, (i + 1) * 2)

        self.assertEqual(seller1.credit, 0.00)
        self.assertEqual(seller2.credit, 0.00)
        self.assertEqual(Transaction.objects.count(), 2000)


local_data = local()


@override_settings(DEBUG=True)
class ConcurrentTest(TestCase):

    def test_concurrent_making_sellers(self):
        def create_user(username):
            Seller.objects.create(name=username, credit=0.00)

        threads = []
        num_threads = 5

        for i in range(num_threads):
            thread = threading.Thread(target=create_user, args=(f'user_{i}',))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(Seller.objects.count(), num_threads)


if __name__ == '__main__':
    unittest.main()
