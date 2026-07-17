# permiso de circulacion
### código para calcular el costo de permiso de circulacion (hecho con gemini):
hay que ingresar manualmente la tasación de cada auto en particular (se obtiene en el SII), con el precio utm de cada año en el mes de enero.

```python
def calcular_permiso_circulacion(tasacion_clp: float, utm_enero: float, es_electrico: bool = False) -> int:
    # 1. Convertir la tasación del vehículo a UTM para evaluar el tramo
    tasacion_utm = tasacion_clp / utm_enero
    
    # 2. Asignar tasa y rebaja según los tramos de la Ley de Rentas Municipales
    if tasacion_utm <= 60.0:
        tasa = 0.015
        rebaja_utm = 0.0
    elif tasacion_utm <= 120.0:
        tasa = 0.020
        rebaja_utm = 0.30
    elif tasacion_utm <= 250.0:
        tasa = 0.030
        rebaja_utm = 1.50
    elif tasacion_utm <= 400.0:
        tasa = 0.045
        rebaja_utm = 5.25
    else:
        tasa = 0.050
        rebaja_utm = 7.25

    # 3. Calcular impuesto base
    impuesto_base = (tasacion_clp * tasa) - (rebaja_utm * utm_enero)
    
    # 4. Validar contra el cobro mínimo de 0.5 UTM
    cobro_minimo = 0.5 * utm_enero
    if impuesto_base < cobro_minimo:
        impuesto_base = cobro_minimo
        
    # 5. Aplicar beneficio de electromovilidad si corresponde (paga el 25%)
    if es_electrico:
        impuesto_base *= 0.25

    # 6. Retornar valor final redondeado a entero (moneda chilena)
    return round(impuesto_base)

# --- EJEMPLO DE USO ---
# Datos de prueba simulados (Ej: Auto de gama media con tasación de $15.000.000)
UTM_ENERO_2026 = 71649.0  # Valor aproximado de referencia
TASACION_AUTO = 15000000.0

monto_final = calcular_permiso_circulacion(TASACION_AUTO, UTM_ENERO_2026)
print(f"Monto a pagar por el Permiso: ${monto_final:,}")
```


anibal