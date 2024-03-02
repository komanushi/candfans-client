from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from candfans_client.async_client import AsyncCandFansClient
from candfans_client.models.timeline import PostType
from candfans_client.models.user import FollowStatus
from tests.utils import mock_session_request


@patch('httpx._client.AsyncClient.request', side_effect=mock_session_request)
class TestAsyncAnonymousCandFansClient(IsolatedAsyncioTestCase):
    async def test_login(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        self.assertTrue(client.logged_in)

    async def test_get_sales_history(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        histories = await client.get_sales_history('2023-11')
        self.assertEqual(len(histories), 2)

    async def test_get_sales(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        sales = await client.get_sales('2023-11')
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].subscribe_sum, 3000)

    async def test_get_sales_purchase_post(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        purchases = await client.get_sales_purchase_post('2023-11')
        self.assertEqual(len(purchases.sales), 2)
        self.assertEqual(purchases.total_price, 300)

    async def test_get_sales_subscribe(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        subscribe = await client.get_sales_subscribe('2023-11')
        self.assertEqual(len(subscribe.sales), 2)
        self.assertEqual(subscribe.total_price, 3000)
        self.assertEqual(subscribe.sales[0].sum_price, 3000)

    async def test_get_sales_chip(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        chip = await client.get_sales_chip('2023-11')
        self.assertEqual(len(chip.sales), 1)
        self.assertEqual(chip.total_price, 1000)
        self.assertEqual(chip.sales[0].sum_price, 1000)

    async def test_get_sales_backnumber(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        backnumber = await client.get_sales_backnumber('2023-11')
        self.assertEqual(len(backnumber.sales), 1)
        self.assertEqual(backnumber.total_price, 2800)
        self.assertEqual(backnumber.sales[0].sum_price, 2800)

    async def test_follows(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        follows = []
        async for f in client.get_follows(999):
            follows.append(f)
        self.assertEqual(len(follows), 2)
        self.assertTrue(follows[0].is_follow)
        self.assertTrue(follows[0].is_official_creator)
        self.assertTrue(follows[1].is_follow)
        self.assertFalse(follows[1].is_official_creator)

    async def test_followed(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        followed = []
        async for f in client.get_followed(999):
            followed.append(f)
        self.assertEqual(len(followed), 2)
        self.assertFalse(followed[0].is_follow)
        self.assertFalse(followed[0].is_official_creator)
        self.assertFalse(followed[1].is_follow)
        self.assertFalse(followed[1].is_official_creator)

    async def test_get_user_mine(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        mine_user_info = await client.get_user_mine()
        self.assertEqual(len(mine_user_info.plans), 2)
        self.assertEqual(len(mine_user_info.users), 1)

    async def test_get_users(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        user_info = await client.get_users('dummy_user')
        self.assertEqual(len(user_info.plans), 2)
        self.assertEqual(user_info.user.user_code, 'dummy_user')

    async def test_get_timeline_month(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        timeline_months = await client.get_timeline_month(9999)
        self.assertEqual(len(timeline_months), 9)
        self.assertEqual(timeline_months[-1].column_name, '2023年06月')
        self.assertEqual(timeline_months[0].column_name, '2024年02月')

    async def test_get_timeline_with_public(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        posts = []
        async for p in client.get_timeline(
            user_id=9999,
            post_types=[PostType.PUBLIC_ITEM],
            month='2024-01'
        ):
            posts.append(p)
        self.assertEqual(len(posts), 2)

    async def test_get_timeline_with_limited_access(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        posts = []
        async for p in client.get_timeline(
            user_id=9999,
            post_types=[PostType.LIMITED_ACCESS_ITEM],
            month='2024-02'
        ):
            posts.append(p)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].plans[0].plan_id, 123)

    async def test_follow(self, *args):
        client = AsyncCandFansClient(
            email='test@test.com',
            password='password'
        )
        await client.login()
        ret = await client.follow(
            user_id=9999,
        )
        self.assertEqual(ret, FollowStatus.FOLLOWED)
