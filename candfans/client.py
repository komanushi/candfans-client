import time
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

    def get_sales_history(self, month_yyyy_mm: str):
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
