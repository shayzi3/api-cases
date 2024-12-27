import redis.asyncio as redis




class RedisPool(redis.Redis):
     def __init__(self):
          super().__init__()

