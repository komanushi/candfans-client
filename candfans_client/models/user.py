from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    user_code: str
    username: str
    profile_img: str
    is_follow: bool
    is_official_creator: bool
    is_on_air: bool
    live_url: str
