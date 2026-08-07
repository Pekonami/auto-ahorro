import os
import json
from typing import Any, Optional
from upstash_redis.asyncio import Redis

#'crearemos una clase encargada de manejar la lectura, escritura y serialización JSON en Redis.'
class RedisService:
    def __init__(self):
        url = os.getenv("UPSTASH_REDIS_REST_URL")
        token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        
        if not url or not token:
            raise ValueError()
            
        # cliente asíncrono para no bloquear la ejecución de FastAPI
        self.client = Redis(url=url, token=token)

    async def get_json(self, key: str) -> Optional[Any]:
        data = await self.client.get(key)
        if data:
            if isinstance(data, str):
                return json.loads(data)
            return data
        return None
    
    async def set_json(self, key: str, value: Any, expire_seconds: int = 21600) -> None:
        json_data = json.dumps(value, ensure_ascii=False)
        await self.client.set(key, json_data, ex=expire_seconds)