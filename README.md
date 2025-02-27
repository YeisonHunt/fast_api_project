# Sistema de Facturación de Energía

Un sistema para calcular y analizar la facturación de energía utilizando Python y PostgreSQL.

## Características

- Calcular conceptos de facturación de energía (EA, EC, EE1, EE2)
- Calcular facturas mensuales para clientes
- Obtener estadísticas de consumo e inyección de clientes
- Monitorear la carga del sistema por hora

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Dependencias listadas en `requirements.txt`

## Estructura del Proyecto

```
energy-billing/
│
├── alembic/                  # Migraciones de base de datos
│   ├── versions/             # Versiones de migración
│   └── env.py                # Configuración del entorno Alembic
│
├── app/                      # Código de la aplicación
│   ├── models/               # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── models.py         # Modelos de la base de datos
│   │
│   ├── routes/               # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── items.py          # Endpoints de facturación de energía
│   │   └── users.py          # Endpoints de usuarios
│   │
│   ├── schemas/              # Modelos Pydantic
│   │   ├── __init__.py
│   │   └── database.py       # Esquemas de solicitud/respuesta
│   │
│   └── utils/                # Funciones utilitarias
│       └── calculations.py   # Lógica de cálculos
│
├── .env                      # Variables de entorno
├── alembic.ini               # Configuración de Alembic
├── database.py               # Configuración de conexión a la base de datos
├── main.py                   # Aplicación FastAPI
└── requirements.txt          # Dependencias del proyecto
```

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/yourusername/energy-billing.git
   cd energy-billing
   ```

2. Crear un entorno virtual:
   ```
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Crear una base de datos PostgreSQL (query console):
   ```
   createdb energy_billing
   ```
   or manual in the UI.

5. Actualizar el archivo `.env` con la URL de conexión a la base de datos:
   ```
   DATABASE_URL=postgresql://usuario:contraseña@localhost/energy_billing
   ```

6. Ejecutar las migraciones:
   ```
   alembic upgrade head
   ```
   
7. Cargar la data inicial desde los CSV:
   ```
   python load_initial_data.py
   ```

## Ejecutar la Aplicación

Iniciar el servidor FastAPI:
```
uvicorn main:app --reload
```

La API estará disponible en http://localhost:8000.

La documentación de la API estará disponible en http://localhost:8000/docs.

### Pruebas con comandos CURL

```sh
# 1. Probar la página de inicio
curl -X GET "http://localhost:8000/"

# 2. Calcular una factura completa para un cliente (Enero 2023)
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "month": 1, "year": 2023}'

# 3. Calcular una factura completa para un cliente (Febrero 2023)
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "month": 2, "year": 2023}'

# 4. Obtener estadísticas de un cliente
curl -X GET "http://localhost:8000/api/v1/client-statistics/1"

# 5. Obtener la carga del sistema para el 1 de enero de 2023
curl -X GET "http://localhost:8000/api/v1/system-load?date_str=2023-01-01"

# 6. Calcular EA (Energía Activa) para enero de 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ea/1?year=2023&month=1"

# 7. Calcular EC (Excedente de Comercialización de Energía) para enero de 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ec/1?year=2023&month=1"

# 8. Calcular EE1 (Excedente de Energía tipo 1) para enero de 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ee1/1?year=2023&month=1"

# 9. Calcular EE2 (Excedente de Energía tipo 2) para enero de 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ee2/1?year=2023&month=1"

# 10. Obtener información básica de un cliente
curl -X GET "http://localhost:8000/api/v1/users/1"

# 11. Probar con otro cliente - cliente 2
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 2, "month": 1, "year": 2023}'
```

## Endpoints de la API

- `POST /api/v1/calculate-invoice`: Calcula la factura de un cliente para un mes específico.
- `GET /api/v1/client-statistics/{client_id}`: Obtiene estadísticas de consumo e inyección de un cliente.
- `GET /api/v1/system-load`: Obtiene la carga del sistema por hora según los datos de consumo.
- `GET /api/v1/calculate-ea/{client_id}`: Calcula EA (Energía Activa) para un cliente y mes.
- `GET /api/v1/calculate-ec/{client_id}`: Calcula EC (Excedente de Comercialización de Energía) para un cliente y mes.
- `GET /api/v1/calculate-ee1/{client_id}`: Calcula EE1 (Excedente de Energía tipo 1) para un cliente y mes.
- `GET /api/v1/calculate-ee2/{client_id}`: Calcula EE2 (Excedente de Energía tipo 2) para un cliente y mes.
- `GET /api/v1/users/{client_id}`: Obtiene información básica de un cliente.

## Esquema de Base de Datos

El esquema de la base de datos incluye las siguientes tablas:
- `services`: Información sobre los servicios de los clientes.
- `records`: Registros de consumo e inyección de energía.
- `consumption`: Datos de consumo de energía.
- `injection`: Datos de inyección de energía.
- `tariffs`: Tarifas de energía.
- `xm_data_hourly_per_agent`: Precios de la energía por hora.

## Lógica de Cálculo

- **EA (Energía Activa)**: Suma del consumo * tarifa CU.
- **EC (Excedente de Comercialización de Energía)**: Suma de la inyección * tarifa C.
- **EE1 (Excedente de Energía tipo 1)**: Min(suma(inyección), suma(consumo)) * (-tarifa CU).
- **EE2 (Excedente de Energía tipo 2)**: Se calcula por hora cuando la inyección supera el consumo.
