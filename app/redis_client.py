import secrets
from decouple import config
import redis

redis_client=redis.Redis.from_url(config('REDIS_URL'),decode_responses=True)

def create_sessions(email:str):
    session_id = secrets.token_hex(20)
    expiry = int(config('EXPIRY'))
    redis_client.setex(f'session:{session_id}',expiry,email)
    return session_id

def get_user_email(session_id:str):
    return redis_client.get(f'session:{session_id}')

def delete_session(session_id:str):
    return redis_client.delete(f'session:{session_id}')