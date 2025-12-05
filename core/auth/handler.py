import time
import jwt
from core.config import settings


secret = settings.JWT_SECRET_KEY
algorithm = "HS256"


def create_access_token(
    user_id: str, time_delta: int = 3600, issue_time: int = None
) -> dict[str, str]:
    if not issue_time:
        issue_time = int(time.time())
    payload = {
        "type": "access",
        "user_id": user_id,
        "expires": issue_time + time_delta,
        "issue_time": issue_time,
    }
    return jwt.encode(payload, secret, algorithm=algorithm)


def create_refresh_token(
    user_id: str, time_delta: int = 3600 * 6, issue_time: int = None
) -> dict[str, str]:
    if not issue_time:
        issue_time = int(time.time())
    payload = {
        "type": "refresh",
        "user_id": user_id,
        "expires": issue_time + time_delta,
        "issue_time": issue_time,
    }
    return jwt.encode(payload, secret, algorithm=algorithm)


def sign_jwt(
    user_id: str, access_time_delta: int = 3600, refresh_time_delta: int = 3600 * 6
) -> dict[str, str]:
    issue_time = int(time.time())
    access = create_access_token(user_id, access_time_delta, issue_time)
    refresh = create_refresh_token(user_id, refresh_time_delta, issue_time)
    return {"access": access, "refresh": refresh}


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, secret, algorithms=[algorithm])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
