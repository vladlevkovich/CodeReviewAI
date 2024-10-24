import json
import os
import redis
from dotenv import load_dotenv

load_dotenv()

class RedisConnect:
    # def __init__(self, host: str = os.getenv('REDIS_HOST'), port: int = os.getenv('REDIS_PORT'), db: int = os.getenv('REDIS_DB')):
    #     # redis://redis:6379/0
    #     self.host = host
    #     self.port = port
    #     self.db = db

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        # redis://redis:6379/0
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        rd = redis.Redis.from_url(f'redis://{self.host}:{self.port}/{self.db}')
        return rd

    def cache(self, key: str, code: str, exp=900):
        # кешуємо на 15 хвилин
        rd = self.connect()
        return rd.set(key, json.dumps(code), ex=exp)

    def get_data(self, key):
        rd = self.connect()
        return rd.get(key)


rd = RedisConnect()
