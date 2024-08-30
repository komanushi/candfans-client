from typing import Optional

from pydantic import BaseModel
from enum import Enum


class CreatorTerm(Enum):
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    TOTALY = 'TOTALY'


class Creator(BaseModel):
    id: int
    user_code: str
    username: str
    profile_img: str
    profile_text: Optional[str]
    follow_cnt: int
    follower_cnt: int
    like_cnt: int
    is_official_creator: bool


class RankingCreator(BaseModel):
    rank: int
    user_id: int
    user_code: str
    username: str
    profile_cover_path: Optional[str]
    profile_icon_path: Optional[str]
    profile_text: Optional[str]
