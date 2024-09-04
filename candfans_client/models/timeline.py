import datetime
from enum import IntEnum
from typing import Optional, List

from pydantic import BaseModel


class PostType(IntEnum):
    PUBLIC_ITEM = 0
    LIMITED_ACCESS_ITEM = 1
    INDIVIDUAL_ITEM = 2
    BACK_NUMBER_ITEM = 3

    @property
    def query_str(self):
        return f'post_type[]={self.value}'


class TimelineMonth(BaseModel):
    column_name: str

    @property
    def formatted_month_str(self) -> str:
        return datetime.datetime.strptime(
            self.column_name, '%Y年%m月'
        ).strftime('%Y-%m')


class ShortPlan(BaseModel):
    plan_id: int
    support_price: int
    total_support_price: int
    plan_name: str
    plan_detail: str
    backnumber_id: Optional[int]
    backnumber_price: Optional[int]
    total_backnumber_price: Optional[int]
    can_see_backnumber_plan_pay: bool
    can_buy_backnumber_not_entry_plan: bool
    add_backnumber_date: Optional[str]
    is_joined_plan: bool


class Post(BaseModel):
    month: str
    post_id: int
    user_id: int
    user_code: str
    username: str
    profile_img: str
    profile_cover_img: str
    post_date: str
    contents_type: int
    post_type: int
    title: str
    contents_text: str
    over_contents_50str: int
    price: int
    limit_post_date: str
    reserve_post_date: str
    contents_path1: str
    contents_path2: str
    contents_path3: str
    contents_path4: str
    image_count: int
    movie_time: Optional[float]
    secret_file: str
    thumbnail_file: str
    like_cnt: int
    comments_cnt: int
    is_like: bool
    can_browsing: bool
    can_send_chip: bool
    apply_status: int
    is_progressed: bool
    is_accept_comment: bool
    can_read_text: bool
    is_official_creator: bool
    has_own_thumbnail: bool
    is_on_air: bool
    live_url: str
    audio_time: Optional[float]
    sample_time: Optional[float]
    thumbnail_file: Optional[str]
    share_count: int
    plans: List[ShortPlan]
