from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class SalesHistory(BaseModel):
    """
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
    """
    orders_id: int
    orders_type: int
    sales_date: datetime
    user_id: int
    user_code: str
    username: str
    profile_img: str
    subscribe_amount: int
    purchase_post_amount: int
    user_chip_amount: int
    post_chip_amount: int
    message_chip_amount: int
    message_amount: int
    backnumber_amount: int
    streaming_amount: int
    subscribe_affiliate_amount: int
    purchase_post_affiliate_amount: int
    affiliate_amount: int
    plan_id: int
    plan_name: str
    support_price: int
    post_id: int
    thread_message_id: int
    purchase_post_id: int
    backnumber_id: int
    backnumber_month: str
    backnumber_plan_name: str


class Sales(BaseModel):
    """
    {
        "chip_user_cnt": 1,
        "chip_user_sum": 2505,
        "chip_post_cnt": 4,
        "chip_post_sum": 11690,
        "chip_message_cnt": 0,
        "chip_message_sum": 0,
        "message_cnt": 0,
        "message_sum": 0,
        "backnumber_cnt": 0,
        "backnumber_sum": 0,
        "streaming_cnt": 0,
        "streaming_sum": 0,
        "purchase_cnt": 0,
        "purchase_sum": 0,
        "subscribe_cnt": 23,
        "subscribe_sum": 24550,
        "affiliate_referrer_cnt": 0,
        "affiliate_referrer_sum": 0
    }
    """
    chip_user_cnt: int
    chip_user_sum: int
    chip_post_cnt: int
    chip_post_sum: int
    chip_message_cnt: int
    chip_message_sum: int
    message_cnt: int
    message_sum: int
    backnumber_cnt: int
    backnumber_sum: int
    streaming_cnt: int
    streaming_sum: int
    purchase_cnt: int
    purchase_sum: int
    subscribe_cnt: int
    subscribe_sum: int
    affiliate_referrer_cnt: int
    affiliate_referrer_sum: int


class PurchaseSale(BaseModel):
    """
    {
        "content": "単品商品名",
        "post_id": 2,
        "created_at": "2023-12-29T00:00:00.000000Z",
        "sum_price": 600,
        "sum_cnt": 1
    }
    """
    content: str
    post_id: int
    created_at: datetime
    sum_price: int
    sum_cnt: int


class SalesPurchasePost(BaseModel):
    """
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
    """
    total_price: int
    sales: List[PurchaseSale]


class SubscribeSale(BaseModel):
    """
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
    """
    plan_id: int
    plan_name: str
    support_price: int
    # 現在の登録者数を示すためその月に関係ない値が入る
    fans_cnt: Optional[int]
    # sum_cnt * support_price * (1 - 手数料比率)に原則なるがクーポンを使っている場合はその分減る
    sum_price: int
    sum_cnt: int
    continue_cnt: int
    new_cnt: int
    withdraw_cnt: int


class SalesSubscribe(BaseModel):
    total_price: int
    sales: List[SubscribeSale]


class ChipSale(BaseModel):
    """
    {
        "username": "UserName",
        "user_code": "UserCode",
        "sum_price": 9999,
        "sum_cnt": 5
    }
    """
    username: str
    user_code: str
    sum_price: int
    sum_cnt: int


class SalesChip(BaseModel):
    total_price: int
    sales: List[ChipSale]


class BacknumberSale(BaseModel):
    """
    {
        "backnumber_id": 1,
        "plan_name": "PlanName",
        "month": "2023年12月",
        "sum_price": 1000,
        "sum_cnt": 2
    }
    """
    backnumber_id: int
    plan_name: str
    month: str
    sum_price: int
    sum_cnt: int


class SalesBacknumber(BaseModel):
    total_price: int
    sales: List[BacknumberSale]
