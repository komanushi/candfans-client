from unittest import TestCase
from unittest.mock import patch

from candfans_client.client import CandFansClient
from utils import mock_session_request


@patch('requests.sessions.Session.request', side_effect=mock_session_request)
class TestClient(TestCase):
    def test_login(self, *args):
        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        self.assertTrue(client.logged_in)

    def test_get_sales_history(self, *args):
        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        histories = client.get_sales_history('2023-11')
        self.assertEqual(len(histories), 2)

    def test_get_sales(self, *args):
        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        sales = client.get_sales('2023-11')
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].subscribe_sum, 3000)

    def test_get_sales_purchase_post(self, *args):
        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        purchases = client.get_sales_purchase_post('2023-11')
        self.assertEqual(len(purchases.sales), 2)
        self.assertEqual(purchases.total_price, 300)

    def test_get_sales_subscribe(self, *args):
        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        subscribe = client.get_sales_subscribe('2023-11')
        self.assertEqual(len(subscribe.sales), 2)
        self.assertEqual(subscribe.total_price, 3000)
        self.assertEqual(subscribe.sales[0].sum_price, 3000)

    def test_get_sales_chip(self, *args):
        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        chip = client.get_sales_chip('2023-11')
        self.assertEqual(len(chip.sales), 1)
        self.assertEqual(chip.total_price, 1000)
        self.assertEqual(chip.sales[0].sum_price, 1000)

    def test_get_sales_backnumber(self, *args):
        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        backnumber = client.get_sales_backnumber('2023-11')
        self.assertEqual(len(backnumber.sales), 1)
        self.assertEqual(backnumber.total_price, 2800)
        self.assertEqual(backnumber.sales[0].sum_price, 2800)