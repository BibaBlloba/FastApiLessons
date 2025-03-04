import asyncio
from typing import Optional

import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        """
        Инициализация RedisManager с указанием хоста и порта Redis.
        """
        self.host = host
        self.port = port
        self.client: redis.Redis

    async def connect(self):
        """
        Асинхронное подключение к серверу Redis.
        """
        self.client = await redis.Redis(
            host=self.host, port=self.port, db=0, decode_responses=True
        )
        await self.client.ping()  # Проверим подключение через ping

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """
        Сохранение ключа с значением в Redis с опциональным временем истечения.

        :param key: Ключ
        :param value: Значение
        :param expire: Время жизни ключа в секундах. Если None, то ключ не истекает.
        """
        if expire:
            await self.client.setex(key, expire, value)
        else:
            await self.client.set(key, value)

    async def get(self, key: str) -> Optional[str]:
        """
        Получение значения по ключу из Redis.

        :param key: Ключ
        :return: Значение или None, если ключ не найден.
        """
        return await self.client.get(key)

    async def delete(self, key: str):
        """
        Удаление ключа из Redis.

        :param key: Ключ для удаления.
        """
        await self.client.delete(key)

    async def close(self):
        """
        Закрытие подключения к Redis.
        """
        await self.client.close()


# Пример использования
async def main():
    redis_manager = RedisManager("localhost", 6379)
    await redis_manager.connect()

    await redis_manager.set("foo", "bar", expire=10)
    value = await redis_manager.get("foo")
    print(f"Значение foo: {value}")

    await redis_manager.delete("foo")
    value_after_delete = await redis_manager.get("foo")
    print(f"Значение foo после удаления: {value_after_delete}")

    await redis_manager.close()


# Запуск
if __name__ == "__main__":
    asyncio.run(main())
