import secrets

from redis import Redis
from src.core.config import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def generate_invite_token():
    return secrets.token_urlsafe(32)


def save_invite_token(email: str, token: str):
    redis.setex(f"invite:{email}", 86400, token)


def verify_invite_token(email: str, token: str):
    stored_token = redis.get(f"invite:{email}")
    print(stored_token)
    if stored_token and stored_token.decode() == token:
        redis.delete(f"invite:{email}")
        return True
    return False
