import time
from typing import List
from urllib.parse import unquote

import requests


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

    def get_sales_history(self, month_yyyy_mm: str) -> List[dict]:
        """
        https://candfans.jp/api/orders/get-sales-history?month=2023-12&page=1
        {
          "status": "SUCCESS",
          "message": "売上履歴を取得しました。",
          "data": [
            {
              "orders_id": 1111,
              "orders_type": 6,
              "sales_date": "2023-11-29 23:44:41",
              "user_id": 111111,
              "user_code": "XXXXXXX",
              "username": "koma",
              "profile_img": "/images/response/no-profile-img.png",
              "subscribe_amount": 9999,
              "purchase_post_amount": 0,
              "user_chip_amount": 0,
              "post_chip_amount": 0,
              "message_chip_amount": 0,
              "message_amount": 0,
              "backnumber_amount": 0,
              "streaming_amount": 0,
              "subscribe_affiliate_amount": 0,
              "purchase_post_affiliate_amount": 0,
              "affiliate_amount": 0,
              "plan_id": 99999,
              "plan_name": "プランネーム",
              "support_price": 9999,
              "post_id": 0,
              "thread_message_id": 0,
              "purchase_post_id": 0,
              "backnumber_id": 0,
              "backnumber_month": "",
              "backnumber_plan_name": ""
            },
        }
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
        return histories

    def get_sales(self, month_yyyy_mm: str):
        """
        {
            "status": "SUCCESS",
            "message": "売上情報を取得しました。",
            "data": [
                {
                    "chip_user_cnt": 0,
                    "chip_user_sum": 0,
                    "chip_post_cnt": 0,
                    "chip_post_sum": 0,
                    "chip_message_cnt": 0,
                    "chip_message_sum": 0,
                    "message_cnt": 0,
                    "message_sum": 0,
                    "backnumber_cnt": 0,
                    "backnumber_sum": 0,
                    "streaming_cnt": 0,
                    "streaming_sum": 0,
                    "purchase_cnt": 10,
                    "purchase_sum": 9999,
                    "purchase_affi_cnt": 0,
                    "purchase_affi_sum": 0,
                    "subscribe_cnt": 10,
                    "subscribe_sum": 9999,
                    "subscribe_affi_cnt": 0,
                    "subscribe_affi_sum": 0,
                    "affiliate_cnt": 0,
                    "affiliate_sum": 0,
                    "affiliate_referrer_cnt": 0,
                    "affiliate_referrer_sum": 0
                }
            ]
        }
        """
        try:
            res_json = self._get(
                f'api/orders/get-sales?month={month_yyyy_mm}',
                headers=self.header
            )
            return res_json['data']
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def get_sales_purchase_post(self, month_yyyy_mm: str):
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
            ]
          }
        }
        """
        try:
            res_json = self._get(
                f'api/orders/get-sales-purchasepost?month={month_yyyy_mm}',
                headers=self.header
            )
            return res_json['data']
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
            return res_json['data']
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def get_sales_chip(self, month_yyyy_mm: str):
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
            return res_json['data']
        except CandFansException as e:
            raise CandFansException(
                f'failed get sales for month {month_yyyy_mm}[{e}]'
            )

    def get_sales_backnumber(self, month_yyyy_mm: str):
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
            return res_json['data']
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
