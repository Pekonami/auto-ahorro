from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any #progra avanzada

#diseñar modelos con pydantic v2

#atts

#distribuidor
class DistribuidorDetail(BaseModel):
    marca: str
    logo: str

#servicios
class ServicesDetail(BaseModel):
    cajero_automatico: bool = Field(alias="Cajero automático")
    bano_publico: bool = Field(alias="Baño público")
    farmacia: bool = Field(alias="Farmacia")
    tienda_de_conveniencia: bool = Field(alias="Tienda de conveniencia")
    compresor_de_aire: bool = Field(alias="Compresor de aire para neumáticos")
    lavado_de_autos: bool = Field(alias="Lavado de autos")
    area_juegos: bool = Field(alias="Área de juegos para menores de edad")
    servicios_mantencion: bool = Field(alias="Servicios mantención")
    surtidor_camiones: bool = Field(alias="Surtidor para camiones")
    duchas: bool = Field(alias="Duchas")
    lubricentro: bool = Field(alias="Lubricentro")
    adblue_granel: bool = Field(alias="AdBlue Granel")
    generador: bool = Field(alias="Generador")

#metodos de pago
class PaymentMethods(BaseModel):
    efectivo: bool = Field(alias="Efectivo")
    cheque: bool = Field(alias="Cheque")
    tarjeta_grandes_tiendas: bool = Field(alias="Tarjeta Grandes Tiendas")
    tarjetas_bancarias: bool = Field(alias="Tarjetas Bancarias")
    tarjeta_credito: bool = Field(alias="Tarjeta de Crédito")
    tarjeta_debito: bool = Field(alias="Tarjeta de Débito")
    app_de_pago: bool = Field(alias="App de pago")
    billetera_digital: bool = Field(alias="Billetera Digital")

#ubicacion
class StationUbicacion(BaseModel):
    nombre_region: str
    codigo_region: str
    nombre_comuna: str
    codigo_comuna: str
    direccion: str
    latitud: str
    longitud: str

#precios
class FuelPriceDetail(BaseModel):
    unidad_cobro: str
    #despues se pasará a decimal
    precio: str 
    fecha_actualizacion: str
    hora_actualizacion: str
    tipo_atencion: str

class EstacionServicioInput(BaseModel):
    codigo: str
    en_mantenimiento: int
    horario_atencion: Optional[str] = None
    razon_social: str
    distribuidor: DistribuidorDetail
    servicios: ServicesDetail
    metodos_de_pago: PaymentMethods
    ubicacion: StationUbicacion
    punto_electrico: List[Dict[str, Any]] = Field(default_factory=list)
    precios: Dict[str, FuelPriceDetail] = Field(default_factory=dict) #pueden existir precios nulos (no se en que caso)