import random
from datetime import timedelta
from fastapi_redis_session.config import basicConfig

REDIS_USERNAME = "default"
REDIS_PWD = "redispw"

basicConfig(
    redisURL='redis://127.0.0.1:49153',
    sessionIdName='sessionId',
    sessionIdGenerator=lambda: str(random.randint(1000, 9999)),
    expireTime=timedelta(days=1)
)