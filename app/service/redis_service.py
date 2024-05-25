import redis


class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def put(self, key, value):
        """
        Set a key in Redis to a specified value.
        """
        self.client.set(key, value)

    def get(self, key):
        """
        Get the value associated with the specified key in Redis.
        """
        return self.client.get(key)

    def delete(self, key):
        """
        Delete a key from Redis.
        """
        self.client.delete(key)

    def save(self):
        """
        Save the current Redis database to disk.
        """
        self.client.save()

    def keys(self, pattern='*'):
        """
        Get all keys matching the specified pattern in Redis.
        """
        return self.client.keys(pattern)


redis_manager = RedisManager("localhost", 6379, 0)
