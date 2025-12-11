from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    full_name: str = ""
    bio: str = ""
    avatar_url: str = ""
    sport: str = ""
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Post:
    id: Optional[int] = None
    user_id: int = 0
    caption: str = ""
    image_url: str = ""
    likes_count: int = 0
    comments_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Joined data from user table
    username: str = ""
    user_avatar: str = ""

@dataclass
class Like:
    id: Optional[int] = None
    user_id: int = 0
    post_id: int = 0
    created_at: Optional[datetime] = None

@dataclass
class Comment:
    id: Optional[int] = None
    user_id: int = 0
    post_id: int = 0
    content: str = ""
    created_at: Optional[datetime] = None
    
    # Joined data
    username: str = ""
    user_avatar: str = ""

@dataclass
class Follow:
    id: Optional[int] = None
    follower_id: int = 0
    following_id: int = 0
    created_at: Optional[datetime] = None