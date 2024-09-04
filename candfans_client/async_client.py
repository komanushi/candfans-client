from __future__ import annotations

import asyncio
import os
import json

from typing import List, Optional, AsyncGenerator
from urllib.parse import quote_plus, unquote

import httpx

from candfans_client.models.sales import SalesHistory, Sales, SalesPurchasePost, SalesSubscribe, SalesChip, \
    SalesBacknumber
from candfans_client.models.search import RankingCreator, CreatorTerm
from candfans_client.models.user import (
    User,
    UserInfo, MineUserInfo, FollowStatus,
)
from candfans_client.models.timeline import (
    Post,
    PostType,
    TimelineMonth,
)
from candfans_client.exceptions import CandFansException


class AsyncAnonymousCandFansClient:

    def __init__(self, base_url: str = 'https://candfans.jp', debug: bool = False):

        self._base_url = base_url
        self._session = httpx.AsyncClient(timeout=httpx.Timeout(5.0, read=20.0))
        self.debug = debug
        if self.debug:
            import logging
            import http.client as http_client

            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            fmt = "[DEBUG LOGGING][%(asctime)s] %(levelname)s %(name)s :%(message)s"
            logging.basicConfig(level=logging.DEBUG, format=fmt)
            http_client.HTTPConnection.debuglevel = 1


    @property
    def base_url(self):
        return self._base_url

    @property
    def header(self):
        base = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://r18.candfans.jp',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        return base

    async def get_follows(
            self, user_id: int, start_page: int = 1, max_page: int = 10
    ) -> AsyncGenerator[User, None]:
        """
        https://candfans.jp/api/user/get-follow/1?page=1
        :return:
        """
        page = start_page
        while True:
            try:
                res_json = await self._get(
                    f'api/user/get-follow/{user_id}?page={page}',
                    headers=self.header
                )
            except CandFansException as e:
                raise CandFansException(
                    f'failed get follows of {user_id} page {page} [{e}]'
                )
            if len(res_json['data']) == 0:
                break

            for f in res_json['data']:
                yield User(**f)

            page += 1
            if page > max_page:
                break
            await asyncio.sleep(0.5)

    async def get_followed(
            self, user_id: int, start_page: int = 1, max_page: int = 10
    ) -> AsyncGenerator[User, None]:
        """
        https://candfans.jp/api/user/get-followed/1?page=1
        :return:
        """
        page = start_page
        while True:
            try:
                res_json = await self._get(
                    f'api/user/get-followed/{user_id}?page={page}',
                    headers=self.header
                )
            except CandFansException as e:
                raise CandFansException(
                    f'failed get followed of {user_id} page {page} [{e}]'
                )
            if len(res_json['data']) == 0:
                break
            for f in res_json['data']:
                yield User(**f)
            page += 1
            if page > max_page:
                break
            await asyncio.sleep(0.5)

    async def get_users(self, user_code: str) -> UserInfo:
        try:
            res_json = await self._get(
                f'api/user/get-users?user_code={user_code}',
                headers=self.header
            )
            return UserInfo(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get_users [{e}]'
            )

    async def get_timeline(
            self,
            user_id: int,
            post_types: List[PostType],
            month: Optional[str] = None,
            start_page: int = 1,
            max_page: int = 10,
    ) -> AsyncGenerator[Post, None]:
        """
        https://candfans.jp/api/contents/get-timeline?user_id=999&post_type[]=0&post_type[]=1

        post_type: [
            0, 全体公開
            1, 限定公開
            2, 単品販売
        ]
        :return:
        """
        page = start_page
        post_types_str = '&'.join([p.query_str for p in post_types])
        query_param = f'user_id={user_id}&{post_types_str}'
        if month is not None:
            query_param += f'&month={month}'

        while True:
            try:
                res_json = await self._get(
                    f'api/contents/get-timeline?{query_param}&page={page}',
                    headers=self.header
                )
            except CandFansException as e:
                raise CandFansException(
                    f'failed get timeline of {query_param} page {page} [{e}]'
                )
            if len(res_json['data']) == 0:
                break
            for p in res_json['data']:
                yield Post(**p)
            page += 1
            if page > max_page:
                break
            await asyncio.sleep(0.5)

    async def get_creator_ranking(
        self,
        start_page: int = 1,
        max_page: int = 10,
        per_page: int = 10,
        terms: CreatorTerm = CreatorTerm.DAILY
    ) -> AsyncGenerator[RankingCreator, None]:
        """
        https://candfans.jp/api/v3/ranking/creator?page=1&per-page=10
        :return:
        """
        page = start_page
        while True:
            try:
                res_json = await self._v3_request(
                    'GET',
                    f'api/v3/ranking/creator?page={page}&per-page={per_page}&terms={terms.value}',
                    headers=self.header
                )
            except CandFansException as e:
                raise CandFansException(
                    f'failed get ranking page {page} per-page {per_page} [{e}]'
                )
            if len(res_json['ranking']) == 0:
                break
            for f in res_json['ranking']:
                user = f['user']
                yield RankingCreator(
                    rank=f['rank'],
                    user_id=user['id'],
                    user_code=user['code'],
                    username=user['name'],
                    profile_cover_path=user['profile_cover_path'],
                    profile_icon_path=user['profile_icon_path'],
                    profile_text=user['profile_text'],
                )
            page += 1
            if page > max_page:
                break
            await asyncio.sleep(0.5)

    async def _post(self, path: str, *arg, **kwargs):
        return await self._request('POST', path, *arg, **kwargs)

    async def _get(self, path: str, *arg, **kwargs):
        return await self._request('GET', path, *arg, **kwargs)

    async def _put(self, path: str, *arg, **kwargs):
        return await self._request('PUT', path, *arg, **kwargs)

    async def _request(self, method: str, path: str, *arg, **kwargs):
        url = f'{self.base_url}/{path}'
        response = await self._session.request(method, url, *arg, **kwargs)
        response_json = response.json()

        if self.debug:
            os.makedirs('./debug', exist_ok=True)
            with open(f'debug/{method}_{quote_plus(url)}.json', mode='w') as f:
                f.write(json.dumps(response_json, indent=4, ensure_ascii=False))

        if 'status' not in response_json:
            print(response_json)
            if 'message' in response_json:
                raise CandFansException(response_json['message'])
            raise CandFansException('unknown error')

        if response_json['status'] != 'SUCCESS':
            raise CandFansException(
                f'failed {method} for {path} message [{response_json["message"]}]'
            )
        return response_json

    async def _v3_request(self, method: str, path: str, *arg, **kwargs):
        url = f'{self.base_url}/{path}'
        response = await self._session.request(method, url, *arg, **kwargs)
        response_json = response.json()

        if self.debug:
            os.makedirs('./debug', exist_ok=True)
            with open(f'debug/{method}_{quote_plus(url)}.json', mode='w') as f:
                f.write(json.dumps(response_json, indent=4, ensure_ascii=False))

        return response_json


class AsyncCandFansClient(AsyncAnonymousCandFansClient):

    def __init__(self, email: str, password: str, base_url: str = 'https://candfans.jp', debug: bool = False) -> None:
        super().__init__(base_url, debug)
        self._email = email
        self._password = password
        self._xsrf_token = None
        self.logged_in = False

    @property
    def header(self):
        base = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://r18.candfans.jp',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        if self._xsrf_token:
            base['X-Xsrf-Token'] = self._xsrf_token
        return base

    async def login(self) -> bool:
        cookies = await self._get_csrf_cookies()
        self._xsrf_token = unquote(cookies['XSRF-TOKEN'])
        try:
            res = await self._post(
                'api/auth/login',
                json={
                    'id': self._email,
                    'password': self._password
                },
                headers=self.header,
            )
            self.logged_in = True
            return True
        except CandFansException as e:
            raise e

    async def get_sales_history(self, month_yyyy_mm: str) -> List[SalesHistory]:
        """
        https://candfans.jp/api/orders/get-sales-history?month=2023-12&page=1
        :return:
        """
        histories = []
        page = 1
        while True:
            try:
                res_json = await self._get(
                    f'api/orders/get-sales-history?month={month_yyyy_mm}&page={page}',
                    headers=self.header
                )
            except CandFansException as e:
                raise CandFansException(
                    f'failed get sales history for month {month_yyyy_mm} page {page} [{e}]'
                )
            if len(res_json['data']) == 0:
                break
            histories += res_json['data']
            await asyncio.sleep(0.5)

            page += 1
        return [SalesHistory(**h) for h in histories]

    async def get_sales(self, month_yyyy_mm: str) -> List[Sales]:
        try:
            res_json = await self._get(
                f'api/orders/get-sales?month={month_yyyy_mm}',
                headers=self.header
            )
            return [Sales(**s) for s in res_json['data']]
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    async def get_sales_purchase_post(self, month_yyyy_mm: str) -> SalesPurchasePost:
        """
        {
          "status": "SUCCESS",
          "message": "売上情報を取得しました。",
          "data": {
            "total_price": 1000,
            "sales": [
              {
                "content": "単品商品名",
                "post_id": 1,
                "created_at": "2023-12-29T00:00:00.000000Z",
                "sum_price": 400,
                "sum_cnt": 4
              },
              {
                "content": "単品商品名",
                "post_id": 2,
                "created_at": "2023-12-29T00:00:00.000000Z",
                "sum_price": 600,
                "sum_cnt": 1
              },
            ]
          }
        }
        """
        try:
            res_json = await self._get(
                f'api/orders/get-sales-purchasepost?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesPurchasePost(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    async def get_sales_subscribe(self, month_yyyy_mm: str) -> SalesSubscribe:
        """
        {
          "status": "SUCCESS",
          "message": "売上情報を取得しました。",
          "data": {
            "total_price": 9999,
            "sales": [
              {
                "plan_id": 1,
                "plan_name": "プラン名",
                "support_price": 1500,
                "fans_cnt": 15,
                "sum_price": 9999,
                "sum_cnt": 30,
                "continue_cnt": 10,
                "new_cnt": 20,
                "withdraw_cnt": 23
              },
            ]
          }
        }
        """
        try:
            res_json = await self._get(
                f'api/orders/get-sales-subscribe?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesSubscribe(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    async def get_sales_chip(self, month_yyyy_mm: str) -> SalesChip:
        """
        {
          "status": "SUCCESS",
          "message": "売上情報を取得しました。",
          "data": {
            "total_price": 9999,
            "sales": [
              {
                "username": "UserName",
                "user_code": "UserCode",
                "sum_price": 9999,
                "sum_cnt": 5
              }
            ]
          }
        }
        """
        try:
            res_json = await self._get(
                f'api/orders/get-sales-chip?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesChip(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    async def get_sales_backnumber(self, month_yyyy_mm: str) -> SalesBacknumber:
        """
        {
          "status": "SUCCESS",
          "message": "売上情報を取得しました。",
          "data": {
            "total_price": 1000,
            "sales": [
              {
                "backnumber_id": 1,
                "plan_name": "PlanName",
                "month": "2023年12月",
                "sum_price": 1000,
                "sum_cnt": 2
              }
            ]
          }
        }
        """
        try:
            res_json = await self._get(
                f'api/orders/get-sales-backnumber?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesBacknumber(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    async def get_user_mine(self) -> MineUserInfo:
        """
        data: {
            plans: [{}],
            users: [{}]
        }
        :return:
        """
        try:
            res_json = await self._get(
                f'api/user/get-user-mine',
                headers=self.header
            )
            return MineUserInfo(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get-user-mine [{e}]'
            )

    async def follow(self, user_id: int) -> FollowStatus:
        try:
            cookies = await self._get_csrf_cookies()
            self._xsrf_token = unquote(cookies['XSRF-TOKEN'])
            res_json = await self._put(
                f'api/user/put-follow/{user_id}',
                headers=self.header
            )
            if res_json['message'] == 'フォローしました。':
                return FollowStatus.FOLLOWED
            if res_json['message'] == 'フォローを解除しました。':
                return FollowStatus.UNFOLLOWED

        except CandFansException as e:
            raise CandFansException(
                f'failed follow of [{user_id}] [{e}]'
            )

    async def _get_csrf_cookies(self):
        url = f'{self._base_url}/api/sanctum/csrf-cookie'
        res = await self._session.get(url)
        cookies = res.cookies
        return cookies
