from unittest import TestCase
from unittest.mock import patch

from candfans_client.client import CandFansClient
from tests.utils import mock_session_request


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

    def test_follows(self, *args):

        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        follows = client.get_follows(999)
        self.assertEqual(len(follows), 2)
        self.assertTrue(follows[0].is_follow)
        self.assertTrue(follows[0].is_official_creator)
        self.assertTrue(follows[1].is_follow)
        self.assertFalse(follows[1].is_official_creator)

    def test_followed(self, *args):

        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        followed = client.get_followed(999)
        self.assertEqual(len(followed), 2)
        self.assertFalse(followed[0].is_follow)
        self.assertFalse(followed[0].is_official_creator)
        self.assertFalse(followed[1].is_follow)
        self.assertFalse(followed[1].is_official_creator)

    def test_get_user_mine(self, *args):

        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        mine_user_info = client.get_user_mine()
        self.assertEqual(len(mine_user_info.plans), 2)
        self.assertEqual(len(mine_user_info.users), 1)

    def test_get_users(self, *args):

        client = CandFansClient(
            email='test@test.com',
            password='password'
        )
        user_info = client.get_users('dummy_user')
        self.assertEqual(len(user_info.plans), 2)
        self.assertEqual(user_info.user.user_code, 'dummy_user')
