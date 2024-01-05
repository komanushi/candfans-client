import time
from typing import List
from urllib.parse import unquote

import requests

from .model import (
    Sales,
    SalesHistory,
    SalesPurchasePost,
    SalesSubscribe,
    SalesChip,
    SalesBacknumber
)


class CandFansException(Exception):
    """ Exception raised when Candfans API """


class CandFansClient:
    def __init__(self, email: str, password: str, base_url: str = 'https://candfans.jp', debug: bool = False) -> None:
        self._email = email
        self._password = password
        self._base_url = base_url
        self._xsrf_token = None
        if debug:
            import logging
            import http.client as http_client

            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            fmt = "[DEBUG LOGGING][%(asctime)s] %(levelname)s %(name)s :%(message)s"
            logging.basicConfig(level=logging.DEBUG, format=fmt)
            http_client.HTTPConnection.debuglevel = 1

        self._session = requests.Session()
        self.login()

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
        if self._xsrf_token:
            base['X-Xsrf-Token'] = self._xsrf_token
        return base

    def login(self) -> bool:
        cookies = self._get_csrf_cookies()
        self._xsrf_token = unquote(cookies['XSRF-TOKEN'])
        try:
            res = self._post(
                'api/auth/login',
                json={
                    'id': self._email,
                    'password': self._password
                },
                headers=self.header,
            )
            return True
        except CandFansException as e:
            raise e

    def get_sales_history(self, month_yyyy_mm: str) -> List[SalesHistory]:
        """
        https://candfans.jp/api/orders/get-sales-history?month=2023-12&page=1
        :return:
        """
        histories = []
        page = 1
        while len(histories) == 0:
            try:
                res_json = self._get(
                    f'api/orders/get-sales-history?month={month_yyyy_mm}&page={page}',
                    headers=self.header
                )
            except CandFansException as e:
                raise CandFansException(
                    f'failed get sales history for month {month_yyyy_mm} page {page} [{e}]'
                )
            histories = histories + res_json['data']
            # 1ページ目が空ということはその月に売上はない
            if page == 1 and len(histories) == 0:
                break
            time.sleep(0.5)
        return [SalesHistory(**h) for h in histories]

    def get_sales(self, month_yyyy_mm: str) -> List[Sales]:
        try:
            res_json = self._get(
                f'api/orders/get-sales?month={month_yyyy_mm}',
                headers=self.header
            )
            return [Sales(**s) for s in res_json['data']]
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def get_sales_purchase_post(self, month_yyyy_mm: str) -> SalesPurchasePost:
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
            res_json = self._get(
                f'api/orders/get-sales-purchasepost?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesPurchasePost(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def get_sales_subscribe(self, month_yyyy_mm: str):
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
            res_json = self._get(
                f'api/orders/get-sales-subscribe?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesSubscribe(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def get_sales_chip(self, month_yyyy_mm: str) -> SalesChip:
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
            res_json = self._get(
                f'api/orders/get-sales-chip?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesChip(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def get_sales_backnumber(self, month_yyyy_mm: str) -> SalesBacknumber:
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
            res_json = self._get(
                f'api/orders/get-sales-backnumber?month={month_yyyy_mm}',
                headers=self.header
            )
            return SalesBacknumber(**res_json['data'])
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def _get_csrf_cookies(self):
        res = self._session.get(f'{self._base_url}/api/sanctum/csrf-cookie')
        cookies = res.cookies
        return cookies

    def _post(self, path: str, *arg, **kwargs):
        return self._request('POST', path, *arg, **kwargs)

    def _get(self, path: str, *arg, **kwargs):
        return self._request('GET', path, *arg, **kwargs)

    def _request(self, method: str, path: str, *arg, **kwargs):
        url = f'{self.base_url}/{path}'
        response = self._session.request(method, url, *arg, **kwargs)
        response_json = response.json()
        if 'status' not in response_json:
            print(response_json)
            raise CandFansException('unknown error')

        if response_json['status'] != 'SUCCESS':
            raise CandFansException(
                f'failed {method} for {path} message [{response_json["message"]}]'
            )
        return response_json
