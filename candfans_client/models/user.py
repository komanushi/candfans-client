from enum import IntEnum

from datetime import datetime
from typing import Optional, List

import dateutil.parser

from pydantic import BaseModel, conint


class FollowStatus(IntEnum):
    FOLLOWED = 0
    UNFOLLOWED = 1


class User(BaseModel):
    user_id: int
    user_code: str
    username: str
    profile_img: str
    is_follow: bool
    is_official_creator: bool
    is_on_air: bool
    live_url: str


class DetailUser(BaseModel):
    id: int
    user_code: str
    email: str
    age: int
    birthday: Optional[datetime]
    username: str
    gender: int
    profile_cover_img: str
    profile_text: str
    profile_img: str
    link_twitter: str
    link_instagram: str
    link_tiktok: str
    link_youtube: str
    link_amazon: str
    link_facebook: str
    link_website: str
    apeal_img1: str
    apeal_img2: str
    apeal_img3: str
    tel: str
    creater_genre: int
    promotion: int
    is_affiliater: bool
    email_auth: bool
    sms_auth: bool
    is_verification_required: bool
    verification_status: int
    affiliate_apply_status: Optional[int]
    promotion_apply_status: Optional[int]
    referrer_code: int
    referrer_verification: int
    show_bank_setting: bool
    can_plan_price_change: bool
    dm_paid_open: bool
    follower_cnt: int
    follow_cnt: int
    fans_cnt: Optional[int]
    is_ban: bool
    delete_at: Optional[datetime]
    is_accept_comment: bool
    is_official_creator: bool
    can_change_backnumber_price: bool
    is_card_change_required: bool
    is_dm_available: bool
    reg_dt: datetime
    is_on_air: bool
    live_url: str
    has_plans: bool

    def __init__(self, **data):
        # YYYY-MM-DD
        if data.get('birthday'):
            data['birthday'] = dateutil.parser.parse(data['birthday'])

        super().__init__(**data)


class Plan(BaseModel):
    plan_id: int
    user_id: int
    thanks_message_template_id: Optional[int]
    plan_name: str
    support_price: int
    total_support_price: int
    plan_detail: str
    status: int
    fans_cnt: Optional[int]
    is_fans: bool
    is_price_update: Optional[int]
    change_support_price: Optional[int]
    content_length: int
    delete_at: Optional[datetime]
    backnumber_price: Optional[int]
    limit_after_backnumber: int
    this_month_after_backnumber: int
    can_see_backnumber_plan_pay: bool
    can_buy_backnumber_not_entry_plan: bool
    done_transfar_backnumber: bool
    done_transfar_limit_backnumber: bool
    entry_disabled: bool
    upper_limit_entry_cnt: Optional[int]


class MineUserInfo(BaseModel):
    users: List[DetailUser]
    plans: List[Plan]


class QueriedUser(BaseModel):
    id: int
    user_code: str
    username: str
    profile_cover_img: str
    profile_text: str
    profile_img: str
    creater_genre: int
    link_twitter: str
    link_instagram: str
    link_tiktok: str
    link_youtube: str
    link_amazon: str
    link_facebook: str
    link_website: str
    apeal_img1: str
    apeal_img2: str
    apeal_img3: str
    follower_cnt: conint(ge=0)
    follow_cnt: conint(ge=0)
    like_cnt: conint(ge=0)
    fans_cnt: Optional[int]
    post_cnt: conint(ge=0)
    image_cnt: conint(ge=0)
    movie_cnt: conint(ge=0)
    is_follow: bool
    is_followed: bool
    is_fansed: bool
    is_block: bool
    is_blocked: bool
    is_ban: bool
    can_send_dm: bool
    delete_at: Optional[str]
    is_accept_comment: bool
    is_official_creator: bool
    is_on_air: bool
    live_url: str


class UserInfo(BaseModel):
    user: QueriedUser
    plans: List[Plan]
