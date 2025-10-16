# TradingPlatform Backtest

Un motor de **backtesting** en Python para estrategias de trading.

## Descripción

Este proyecto proporciona la infraestructura básica para cargar datos de mercado, definir estrategias y ejecutar backtests de forma configurada y reproducible.

## Estructura del proyecto

```text
app/                     Carpeta principal de la aplicación
  ├── main.py            Punto de entrada (script o servidor API)
  ├── api/               Endpoints de la API (ej. FastAPI)
  ├── core/              Configuración y dependencias compartidas
  ├── data/              Carga y procesamiento de datos de mercado
  ├── models/            Modelos y clases de dominio (por ejemplo Backtest)
  └── services/          Lógica de negocio y servicios (ej. estrategia, backtest)

tests/                   Pruebas unitarias (pytest)
.env                     Variables de entorno (configuración de API, rutas, etc.)
README.md                Documentación de proyecto
```

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repo>
   cd backtest
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalar dependencias:

   ```bash
   pip install pydantic-settings pytest
   ```

## Configuración

En el archivo raíz, crea o ajusta el fichero `.env` con la clave:

```dotenv
BASE_URL_API_CONNECT=http://localhost:8080/api/v1/market-data
```

## Uso

Dependiendo de la implementación de `app/main.py`, puedes ejecutar:

```bash
python -m app.main
```

O, si has creado una API (por ejemplo con FastAPI):

```bash
uvicorn app.main:app --reload
```

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest
```

## Contribuir

¡Las contribuciones son bienvenidas! Abre issues o pull requests indicando mejoras en estrategias, formatos de datos o nuevos servicios.

## Licencia

Este proyecto está bajo licencia MIT.
  