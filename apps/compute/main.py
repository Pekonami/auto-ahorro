#hecho con ia
#para testear el modelo hecho en pydantic
import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from typing import List
import json

from models.cne import EstacionServicioInput

load_dotenv()

app = FastAPI(
    title="AutoAhorro Compute Service",
    description="Microservicio de cómputo y agregación de datos para AutoAhorro"
)

API_CNE_TOKEN = os.getenv("API_CNE")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "AutoAhorro Compute Engine"}

@app.get("/test-cne/providencia", response_model=List[EstacionServicioInput])
async def test_cne_providencia():
    if not API_CNE_TOKEN:
        raise HTTPException(
            status_code=500, 
            detail="Token de API_CNE no configurado en el archivo .env"
        )

    headers = {
        "Authorization": f"Bearer {API_CNE_TOKEN}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.cne.cl/api/v4/estaciones", headers=headers, timeout=30.0)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Error HTTP en CNE: {response.status_code}"
                )

            # httpx ya descomprime gzip y parsea el JSON
            raw_data = response.json()

            # 1. DEFENSA: Si la API envió un diccionario (posible error oculto o wrapper)
            if isinstance(raw_data, dict):
                if "data" in raw_data:
                    raw_data = raw_data["data"]
                elif "estaciones" in raw_data:
                    raw_data = raw_data["estaciones"]
                else:
                    # Si cae aquí, la API está enviando un mensaje de error. 
                    # Lo lanzamos para que lo veas en Swagger UI.
                    raise ValueError(f"La API respondió con un diccionario inesperado: {raw_data}")

            # 2. DEFENSA: Si la API envió un JSON doblemente serializado (string)
            if isinstance(raw_data, str):
                raw_data = json.loads(raw_data)
                
            # 3. Validar que finalmente tengamos una lista
            if not isinstance(raw_data, list):
                raise ValueError(f"Se esperaba una lista, pero se recibió un {type(raw_data)}")

            # Validación masiva
            estaciones_validadas = []
            for item in raw_data:
                # Si el nodo interno es un string, lo convertimos
                if isinstance(item, str):
                    item = json.loads(item)
                
                estaciones_validadas.append(EstacionServicioInput(**item))

            # Filtrado por comuna
            providencia_stations = [
                e for e in estaciones_validadas 
                if e.ubicacion.nombre_region == "Metropolitana de Santiago" 
                and e.ubicacion.nombre_comuna == "Providencia"
            ]

            return providencia_stations

        except Exception as e:
            # Ahora Swagger te mostrará exactamente qué hay dentro del error
            raise HTTPException(status_code=500, detail=f"Error procesando datos: {str(e)}")