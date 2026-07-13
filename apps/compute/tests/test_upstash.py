import os
from upstash_redis import Redis
import dotenv
config = dotenv.dotenv_values(".env")

url = config.get("UPSTASH_REDIS_REST_URL")
token = config.get("UPSTASH_REDIS_REST_TOKEN")
redis = Redis(url=url, token=token)

try:
    redis.set("llave_prueba", "¡Conexión exitosa desde Python!")
    print("Dato guardado correctamente.")

    valor = redis.get("llave_prueba")
    print(f"Dato recuperado: {valor}")

except Exception as e:
    print(f"Error al conectar con Redis: {e}")
