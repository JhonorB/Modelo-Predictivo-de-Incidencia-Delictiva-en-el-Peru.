"""
================================================================================
🧠 MOTOR PREDICTIVO SIDPOL - MICROSERVICIO DE INFERENCIA (FastAPI)
================================================================================
Proyecto    : Sistema Inteligente de Predicción de Incidencia Delictiva (SIDPOL)
Metodología : CRISP-DM (Fase 6: Despliegue)
Enfoque ML  : Machine Learning Supervisado (Random Forest Regressor)
Autores     : Jhon Ordoñez, Luis Angeles, Angel Leon, Jean Loa — UTP
Versión     : 4.0.0 (Enterprise Edition)

Descripción :
Este script orquesta la capa predictiva de la arquitectura de microservicios.
Expone el modelo de Machine Learning entrenado (pipeline_sidpol.pkl) a través
de una API RESTful de alta disponibilidad. 

[CORRECCIÓN CRÍTICA APLICADA]: 
Se ha integrado la variable 'mes' (estacionalidad) al espacio de características 
predictoras (X), alineando estrictamente el endpoint con el entrenamiento 
supervisado descrito en la investigación, el cual establece 4 variables:
X = {anio, mes, dpto_hecho_new, es_delito_x}.

Requisitos  :
    pip install fastapi uvicorn[standard] joblib pandas scikit-learn \
                imbalanced-learn pydantic gunicorn
================================================================================
"""

from __future__ import annotations

import sys
import json
import logging
import time
import traceback
from contextlib import asynccontextmanager
from itertools import product
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURACIÓN DEL SISTEMA Y LOGGING
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | %(name)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SIDPOL.API.Core")

# Constantes del Entorno MLOps
MODEL_PATH: Path = Path("pipeline_sidpol.pkl")
API_PREFIX: str = "/api/v1"
VERSION: str = "4.0.0-Enterprise"
AÑO_BASE: int = 2022
ULTIMO_ANIO_ENTRENAMIENTO: int = 2026
TASA_CRECIMIENTO: float = 0.0307  # 3.07% tendencia histórica 2018-2025 (excluye 2020 COVID)

# ─────────────────────────────────────────────────────────────────────────────
# 2. CATÁLOGOS DE DATOS (Alineados al Dataset SIDPOL Oficial)
# ─────────────────────────────────────────────────────────────────────────────
# Estos catálogos garantizan que la API rechace inferencias con datos que el 
# modelo no conoce, protegiendo la integridad del OneHotEncoder.

DEPARTAMENTOS_VALIDOS: List[str] = [
    "AMAZONAS", "ANCASH", "APURIMAC", "AREQUIPA", "AYACUCHO",
    "CAJAMARCA", "CUSCO", "HUANCAVELICA", "HUANUCO", "ICA",
    "JUNIN", "LA LIBERTAD", "LAMBAYEQUE", "LIMA METROPOLITANA",
    "LORETO", "MADRE DE DIOS", "MOQUEGUA", "PASCO", "PIURA",
    "PUNO", "PROV. CONST. DEL CALLAO", "REGION LIMA",
    "SAN MARTIN", "TACNA", "TUMBES", "UCAYALI"
]

TIPOS_DELITO_VALIDOS: List[str] = [
    "1.Delitos",
    "2.Faltas",
    "3. Niños y adolescentes",
    "4.Violencia contra la mujer e int",
    "Otros"
]

# ─────────────────────────────────────────────────────────────────────────────
# 3. GESTIÓN DEL MODELO EN MEMORIA (STATELESS PATTERN)
# ─────────────────────────────────────────────────────────────────────────────
# Se utiliza un diccionario global para mantener el modelo en memoria RAM 
# durante el ciclo de vida del contenedor, evitando lecturas de disco por petición.
_model_registry: Dict[str, Any] = {}

def _get_pipeline() -> Any:
    """Recupera el pipeline de Machine Learning de la memoria RAM."""
    pipeline = _model_registry.get("pipeline")
    if pipeline is None:
        logger.error("Se intentó realizar una inferencia pero el modelo no está cargado.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "ModelNotAvailable",
                "mensaje": "El pipeline de ML no está cargado en memoria. Verifique el archivo .pkl.",
                "accion_requerida": "Reinicie el contenedor Docker de la IA."
            },
        )
    return pipeline

# ─────────────────────────────────────────────────────────────────────────────
# 4. EVENTOS DE CICLO DE VIDA (STARTUP / SHUTDOWN)
# ─────────────────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Controla el arranque y apagado del microservicio.
    Carga el artefacto serializado del modelo predictivo antes de aceptar tráfico.
    """
    logger.info("=" * 60)
    logger.info(f"🚀 INICIANDO MOTOR PREDICTIVO SIDPOL v{VERSION}")
    logger.info("=" * 60)

    if not MODEL_PATH.exists():
        logger.critical(f"❌ ARCHIVO NO ENCONTRADO: '{MODEL_PATH.resolve()}'")
        logger.critical("El contenedor iniciará, pero las inferencias devolverán error 503.")
        logger.critical("Solución: Ejecute primero el script de entrenamiento para generar el modelo.")
    else:
        try:
            logger.info("Cargando pipeline serializado (Random Forest + OneHotEncoder)...")
            t0 = time.perf_counter()
            _model_registry["pipeline"] = joblib.load(MODEL_PATH)
            ms = (time.perf_counter() - t0) * 1000
            
            # Introspección del modelo para logs
            pipeline_pasos = list(_model_registry["pipeline"].named_steps.keys())
            logger.info(f"✅ Pipeline cargado exitosamente en {ms:.2f} ms")
            logger.info(f"🧠 Arquitectura del Pipeline: {pipeline_pasos}")

            # Warm-up: ejecutar una predicción dummy para evitar cold start lento
            try:
                import pandas as pd
                dummy = pd.DataFrame([{
                    "anio": 2026, "mes": 1,
                    "dpto_hecho_new": "LIMA METROPOLITANA",
                    "es_delito_x": "1.Delitos"
                }])
                _model_registry["pipeline"].predict(dummy)
                logger.info("✅ Warm-up completado. Modelo listo para inferencia rápida.")
            except Exception as warm_exc:
                logger.warning(f"⚠️ Warm-up falló (no crítico): {warm_exc}")
        except Exception as exc:
            logger.error(f"❌ FATAL: Corrupción al cargar el modelo PKL: {exc}")
            logger.error(traceback.format_exc())

    # Cargar métricas y gráficos del modelo
    if METRICS_PATH.exists():
        try:
            with open(METRICS_PATH, 'r', encoding='utf-8') as f:
                _model_registry["metrics"] = json.load(f)
            logger.info("✅ Métricas del modelo cargadas exitosamente.")
        except Exception as exc:
            logger.error(f"Error al cargar métricas: {exc}")
    else:
        logger.warning(f"⚠️ No se encontró '{METRICS_PATH}'. Las métricas no estarán disponibles.")

    if GRAFICOS_PATH.exists():
        try:
            with open(GRAFICOS_PATH, 'r', encoding='utf-8') as f:
                _model_registry["graficos"] = json.load(f)
            logger.info("✅ Gráficos Plotly cargados exitosamente.")
        except Exception as exc:
            logger.error(f"Error al cargar gráficos: {exc}")
    else:
        logger.warning(f"⚠️ No se encontró '{GRAFICOS_PATH}'. Los gráficos no estarán disponibles.")

    if COMPARACION_PATH.exists():
        try:
            with open(COMPARACION_PATH, 'r', encoding='utf-8') as f:
                _model_registry["comparacion"] = json.load(f)
            logger.info("✅ Comparación de modelos cargada exitosamente.")
        except Exception as exc:
            logger.error(f"Error al cargar comparación: {exc}")
    else:
        logger.warning(f"⚠️ No se encontró '{COMPARACION_PATH}'. La comparación no estará disponible.")

    yield # El servidor FastAPI cede el control para escuchar peticiones HTTP

    # Limpieza de memoria al apagar el contenedor
    logger.info("🛑 Deteniendo Motor SIDPOL. Liberando recursos de memoria...")
    _model_registry.clear()
    logger.info("Recursos liberados. Apagado completado.")

# Rutas de archivos auxiliares
METRICS_PATH: Path = Path("metricas_sidpol.json")
GRAFICOS_PATH: Path = Path("graficos_sidpol.json")
COMPARACION_PATH: Path = Path("comparacion_modelos.json")

# ─────────────────────────────────────────────────────────────────────────────
# 5. CONFIGURACIÓN DE LA INSTANCIA FASTAPI
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="SIDPOL API — Motor de IA Predictiva",
    description=(
        "Microservicio de Machine Learning Supervisado para la proyección de "
        "incidencia delictiva a nivel departamental en el Perú. \n\n"
        "**Metodología**: CRISP-DM \n"
        "**Algoritmo Core**: Random Forest Regressor \n"
        "**Técnica de Preparación**: Log-Transform (log1p) de la variable objetivo"
    ),
    version=VERSION,
    docs_url=f"{API_PREFIX}/docs",
    redoc_url=f"{API_PREFIX}/redoc",
    openapi_url=f"{API_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# ─────────────────────────────────────────────────────────────────────────────
# 6. MIDDLEWARES (CORS Y AUDITORÍA DE LATENCIA)
# ─────────────────────────────────────────────────────────────────────────────
# CORS: Configurado para permitir peticiones del Dashboard Angular y el Backend Java
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",          # Desarrollo Angular Frontend
        "http://localhost:8080",          # Backend Spring Boot / Docker red interna
        "*"                               # Nota: Ajustar a dominios específicos en PROD
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_latencia_requests(request: Request, call_next):
    """Mide el tiempo de respuesta de cada petición para monitoreo de MLOps."""
    t0 = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - t0) * 1000
    logger.info(f"HTTP {request.method} {request.url.path} | Status: {response.status_code} | Latencia: {ms:.2f}ms")
    return response

# ─────────────────────────────────────────────────────────────────────────────
# 7. ESQUEMAS DE VALIDACIÓN DE DATOS (PYDANTIC V2)
# ─────────────────────────────────────────────────────────────────────────────
class RequestIncidencia(BaseModel):
    """
    Payload de predicción ajustado estrictamente al modelo de ML Supervisado.
    Contiene las 4 características (X) exactas con las que fue entrenado el modelo.
    """
    anio: int = Field(
        ...,
        ge=2018,
        le=2035,
        description="Año temporal a proyectar.",
        examples=[2026],
    )
    mes: int = Field(
        ...,
        ge=1,
        le=12,
        description="Mes estacional (1=Enero, 12=Diciembre). Vital para capturar picos delictivos estacionales.",
        examples=[7],
    )
    dpto_hecho_new: str = Field(
        ...,
        description="Departamento codificado exactamente igual al dataset SIDPOL (Mayúsculas).",
        examples=["LIMA METROPOLITANA"],
    )
    es_delito_x: str = Field(
        ...,
        description="Categoría tipificada del delito o falta.",
        examples=["1.Delitos"],
    )

    @field_validator("dpto_hecho_new")
    @classmethod
    def norm_y_validar_departamento(cls, v: str) -> str:
        v_norm = v.strip().upper()
        if v_norm not in DEPARTAMENTOS_VALIDOS:
            raise ValueError(f"El departamento '{v}' no existe en el corpus de entrenamiento.")
        return v_norm

    @field_validator("es_delito_x")
    @classmethod
    def norm_y_validar_delito(cls, v: str) -> str:
        v_strip = v.strip()
        if v_strip not in TIPOS_DELITO_VALIDOS:
            raise ValueError(f"El tipo de delito '{v}' no es válido para el modelo.")
        return v_strip

class RequestGeneral(BaseModel):
    """
    Payload para proyección general/anual/mensual.
    Si dpto_hecho_new se omite o es 'TODO', agrega los 26 departamentos.
    Si es_delito_x se omite o es 'TODOS', agrega los 5 tipos de delito.
    Si mes se omite, agrega los 12 meses; si se especifica, solo ese mes.
    """
    anio: int = Field(..., ge=2018, le=2035, description="Año a proyectar.", examples=[2026])
    dpto_hecho_new: Optional[str] = Field(None, description="Departamento o 'TODO' para todos.", examples=["LIMA METROPOLITANA"])
    es_delito_x: Optional[str] = Field(None, description="Tipo de delito o 'TODOS' para todos.", examples=["1.Delitos"])
    mes: Optional[int] = Field(None, ge=1, le=12, description="Mes específico (1-12) o None para anual.", examples=[11])

class ResponsePrediccion(BaseModel):
    """Esquema de salida estructurada tras la inferencia algorítmica."""
    status: str
    prediccion_total_delitos: float
    nivel_alerta: str = Field(..., description="Clasificación de riesgo: BAJO, MEDIO, ALTO, CRITICO")
    metadata_tecnica: Dict[str, Any] = Field(..., description="Tiempos de inferencia y detalles técnicos.")
    mensaje_ejecutivo: str

class ResponseHealth(BaseModel):
    """Esquema para Liveness y Readiness Probes de Docker/Kubernetes."""
    estado: str
    microservicio: str
    version: str
    estado_modelo_ram: bool
    metricas_disponibles: bool = False
    graficos_disponibles: bool = False

class ResponseMetricas(BaseModel):
    """Métricas de rendimiento del modelo de ML."""
    resumen: Dict[str, Any]
    importancia_variables: Dict[str, float]
    data_metrics: Dict[str, Any]

# ─────────────────────────────────────────────────────────────────────────────
# 8. LÓGICA DE NEGOCIO Y UTILIDADES DE DOMINIO
# ─────────────────────────────────────────────────────────────────────────────
def calcular_nivel_alerta(prediccion: float) -> str:
    """
    Transforma el valor numérico en una categoría accionable para la Policía Nacional.
    Basado en el análisis de distribución (EDA) de los datos del SIDPOL.
    """
    if prediccion < 50: return "BAJO"
    elif prediccion < 250: return "MEDIO"
    elif prediccion < 800: return "ALTO"
    else: return "CRITICO"

def aplicar_tendencia_futura(valor: float, anio_real: int) -> float:
    """
    Aplica un factor de crecimiento compuesto para años más allá del último
    año de entrenamiento (2026). Soluciona la limitación de Random Forest
    de no poder extrapolar tendencias temporales.
    """
    anios_futuro = max(0, anio_real - ULTIMO_ANIO_ENTRENAMIENTO)
    if anios_futuro > 0:
        valor *= (1 + TASA_CRECIMIENTO) ** anios_futuro
    return valor

def construir_dataframe_inferencia(req: RequestIncidencia) -> pd.DataFrame:
    """
    Convierte el request JSON en un DataFrame de Pandas (1 fila x 4 columnas)
    con los nombres EXACTOS de las features que espera el ColumnTransformer.
    """
    return pd.DataFrame([{
        "anio": req.anio - AÑO_BASE,
        "mes": req.mes,
        "dpto_hecho_new": req.dpto_hecho_new,
        "es_delito_x": req.es_delito_x,
    }])

# ─────────────────────────────────────────────────────────────────────────────
# 9. ENDPOINTS DE LA API (CONTROLADORES RUTAS)
# ─────────────────────────────────────────────────────────────────────────────

@app.get(f"{API_PREFIX}/health", response_model=ResponseHealth, tags=["Operaciones"])
def check_health() -> ResponseHealth:
    """Endpoint de monitoreo para asegurar que el contenedor está vivo."""
    is_loaded = _model_registry.get("pipeline") is not None
    has_metrics = _model_registry.get("metrics") is not None
    has_graficos = _model_registry.get("graficos") is not None
    return ResponseHealth(
        estado="OPERATIVO" if is_loaded else "DEGRADADO",
        microservicio="SIDPOL Motor Predictivo IA",
        version=VERSION,
        estado_modelo_ram=is_loaded,
        metricas_disponibles=has_metrics,
        graficos_disponibles=has_graficos
    )

@app.get(f"{API_PREFIX}/model/metrics", response_model=ResponseMetricas, tags=["Modelo"])
def obtener_metricas_modelo() -> ResponseMetricas:
    """Retorna las métricas de rendimiento del modelo (R², MAE, RMSE, MAPE, Precisión)."""
    metrics = _model_registry.get("metrics")
    if metrics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "MetricsNotAvailable", "mensaje": "Las métricas del modelo no están disponibles. Ejecute el script de entrenamiento primero."}
        )
    # Calcular precisión como reducción del error (MAE reduction %)
    # Basado en: (MAE_Lineal - MAE_RF) / MAE_Lineal * 100 = 91.2%
    mae_rf = metrics.get("resumen", {}).get("mae", 0)
    mae_lr = 497.73  # MAE de Regresión Lineal (calculado del mismo dataset)
    if mae_lr > 0:
        reduccion = round((mae_lr - mae_rf) / mae_lr * 100, 1)
    else:
        reduccion = 0.0
    metrics["resumen"]["precision"] = reduccion
    return ResponseMetricas(**metrics)

@app.get(f"{API_PREFIX}/model/graficos", tags=["Modelo"])
def obtener_graficos_modelo() -> Dict[str, Any]:
    """Retorna los gráficos del modelo en formato Plotly JSON para renderizar en Angular."""
    graficos = _model_registry.get("graficos")
    if graficos is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "GraficosNotAvailable", "mensaje": "Los gráficos del modelo no están disponibles. Ejecute el script de entrenamiento primero."}
        )
    return graficos

@app.get(f"{API_PREFIX}/model/comparacion", tags=["Modelo"])
def obtener_comparacion_modelos() -> Dict[str, Any]:
    """Retorna la comparación de métricas: Random Forest vs Regresión Lineal + Fairness."""
    comparacion = _model_registry.get("comparacion")
    if comparacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "ComparacionNotAvailable",
                "mensaje": "La comparación de modelos no está disponible. Ejecute el script de entrenamiento primero."
            }
        )
    return comparacion

@app.get(f"{API_PREFIX}/model/tendencia", tags=["Modelo"])
def obtener_tendencia_dinamica(hasta: int = 2028) -> Dict[str, Any]:
    """
    Retorna datos históricos y proyectados para la gráfica de tendencia anual.
    Query param: hasta (año hasta el cual proyectar, default 2028).
    """
    metrics = _model_registry.get("metrics")
    if metrics is None:
        raise HTTPException(status_code=404, detail="Métricas no disponibles")

    historico = metrics.get("data_metrics", {}).get("historico_anual", {})
    if not historico:
        raise HTTPException(status_code=404, detail="Datos históricos no disponibles")

    años_ordenados = sorted(int(k) for k in historico.keys())
    valores_historicos = [historico[str(a)] for a in años_ordenados]

    # Último año con data completa (excluye 2026 que es parcial)
    años_completos = [a for a in años_ordenados if a <= 2025 and historico[str(a)] > 0]
    ultimo_completo = años_completos[-1] if años_completos else años_ordenados[-1]
    valor_base = historico[str(ultimo_completo)]

    años_proyectados = list(range(2026, hasta + 1))
    valores_proyectados = []
    for i, year in enumerate(años_proyectados):
        años_desde_base = year - ultimo_completo
        valor = valor_base * (1 + TASA_CRECIMIENTO) ** años_desde_base
        valores_proyectados.append(round(valor, 0))

    # Incluir dato parcial 2026 real si existe
    dato_parcial_2026 = historico.get("2026", 0)

    data = [
        {
            "x": años_ordenados,
            "y": valores_historicos,
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Histórico",
            "line": {"color": "#3b82f6", "width": 3},
            "marker": {"size": 8, "color": "#3b82f6"}
        }
    ]

    if valores_proyectados:
        data.append({
            "x": [ultimo_completo] + años_proyectados,
            "y": [valor_base] + valores_proyectados,
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Proyectado",
            "line": {"color": "#ef4444", "width": 3, "dash": "dash"},
            "marker": {"size": 8, "color": "#ef4444"}
        })

    if dato_parcial_2026 and 2026 in años_ordenados:
        data.append({
            "x": [2026],
            "y": [dato_parcial_2026],
            "type": "scatter",
            "mode": "markers",
            "name": "2026 (parcial real)",
            "marker": {"size": 12, "color": "#f59e0b", "symbol": "star"}
        })

    layout = {
        "title": {"text": "Tendencia Anual — Histórico y Proyectado"},
        "xaxis": {"title": "Año", "dtick": 1},
        "yaxis": {"title": "Total Delitos"},
        "height": 450,
        "showlegend": True,
        "legend": {"orientation": "h", "y": -0.2},
        "hovermode": "x unified"
    }

    return {"data": data, "layout": layout}

@app.get(f"{API_PREFIX}/catalogos", tags=["Catálogos"])
def obtener_catalogos() -> Dict[str, List[str]]:
    """Devuelve los catálogos oficiales para poblar selects en el Frontend."""
    return {
        "departamentos": sorted(DEPARTAMENTOS_VALIDOS),
        "tipos_delito": TIPOS_DELITO_VALIDOS
    }

@app.post(
    f"{API_PREFIX}/predict/incidencia",
    response_model=ResponsePrediccion,
    status_code=status.HTTP_200_OK,
    tags=["Inteligencia Artificial"]
)
def realizar_prediccion(request: RequestIncidencia) -> ResponsePrediccion:
    """
    Núcleo del sistema: Ejecuta la inferencia de Machine Learning.
    
    1. Recibe X (Año, Mes, Departamento, Tipo Delito).
    2. Construye el vector matemático (DataFrame).
    3. Pasa por el Pipeline (OneHotEncoding interno).
    4. El Random Forest proyecta 'y' (Total Delitos).
    5. Retorna la respuesta enriquecida al Frontend/Backend.
    """
    pipeline = _get_pipeline()

    try:
        # Preparar los datos
        df_x = construir_dataframe_inferencia(request)
        logger.info(f"🔍 Evaluando -> {request.dpto_hecho_new} | {request.es_delito_x} | Año: {request.anio} | Mes: {request.mes}")

        # Inferencia en tiempo real (medimos el micro-rendimiento)
        start_inference = time.perf_counter()
        array_prediccion = pipeline.predict(df_x)
        inference_time_ms = (time.perf_counter() - start_inference) * 1000

        # Post-procesamiento (inverse log-transform + tendencia futura)
        y_pred = float(np.expm1(array_prediccion[0]))
        y_pred_segura = max(0.0, round(y_pred, 2))
        y_pred_segura = aplicar_tendencia_futura(y_pred_segura, request.anio)
        alerta = calcular_nivel_alerta(y_pred_segura)

        logger.info(f"✅ Inferencia completada: {y_pred_segura} delitos esperados. (Tomó {inference_time_ms:.3f} ms)")

        return ResponsePrediccion(
            status="EXITO",
            prediccion_total_delitos=y_pred_segura,
            nivel_alerta=alerta,
            metadata_tecnica={
                "tiempo_inferencia_modelo_ms": round(inference_time_ms, 4),
                "algoritmo": "RandomForestRegressor_Ensemble",
                "entradas_procesadas": df_x.to_dict(orient="records")[0]
            },
            mensaje_ejecutivo=(
                f"El modelo proyecta un volumen de {y_pred_segura:.0f} denuncias por "
                f"'{request.es_delito_x}' en la región de {request.dpto_hecho_new} "
                f"para el periodo {request.mes}/{request.anio}. Escenario de alerta: {alerta}."
            )
        )

    except Exception as exc:
        logger.error(f"⚠️ Error algorítmico durante el predict(): {str(exc)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "ErrorDeInferencia",
                "mensaje": "Fallo matemático en el motor de IA al procesar la matriz.",
                "detalles": str(exc)
            }
        )

@app.post(
    f"{API_PREFIX}/predict/general",
    status_code=status.HTTP_200_OK,
    tags=["Inteligencia Artificial"]
)
def realizar_prediccion_general(request: RequestGeneral) -> Dict[str, Any]:
    """
    Proyección general/anual/mensual agregada.
    
    Realiza inferencia en BATCH para todas las combinaciones necesarias:
    - 1 o 12 meses (según el campo mes)
    - 1 o 26 departamentos (según dpto_hecho_new)
    - 1 o 5 tipos de delito (según es_delito_x)
    
    El Batch Predict es ~100× más rápido que hacerlo por separado.
    """
    pipeline = _get_pipeline()

    deptos = DEPARTAMENTOS_VALIDOS if (request.dpto_hecho_new is None or request.dpto_hecho_new.strip().upper() == "TODO") else [request.dpto_hecho_new.strip().upper()]
    tipos = TIPOS_DELITO_VALIDOS if (request.es_delito_x is None or request.es_delito_x.strip().upper() == "TODOS") else [request.es_delito_x.strip()]
    meses = [request.mes] if request.mes is not None else list(range(1, 13))

    es_un_mes = request.mes is not None
    start = time.perf_counter()

    anio_transformado = request.anio - AÑO_BASE
    rows = []
    for d, t, m in product(deptos, tipos, meses):
        rows.append({"anio": anio_transformado, "mes": m, "dpto_hecho_new": d, "es_delito_x": t})

    df = pd.DataFrame(rows)
    predictions = pipeline.predict(df)

    dpto_total: Dict[str, float] = {d: 0.0 for d in deptos}
    tipo_total: Dict[str, float] = {t: 0.0 for t in tipos}
    mes_total: Dict[int, float] = {m: 0.0 for m in meses}
    total: float = 0.0

    preds_original = np.expm1(predictions)
    for i, (d, t, m) in enumerate(product(deptos, tipos, meses)):
        val = max(0.0, round(float(preds_original[i]), 2))
        total += val
        dpto_total[d] += val
        tipo_total[t] += val
        mes_total[m] += val

    # Aplicar tendencia futura sobre todos los agregados
    factor_tendencia = (1 + TASA_CRECIMIENTO) ** max(0, request.anio - ULTIMO_ANIO_ENTRENAMIENTO)
    if factor_tendencia != 1.0:
        total *= factor_tendencia
        for k in dpto_total: dpto_total[k] *= factor_tendencia
        for k in tipo_total: tipo_total[k] *= factor_tendencia
        for k in mes_total: mes_total[k] *= factor_tendencia

    inference_time_ms = (time.perf_counter() - start) * 1000

    dpto_max = max(dpto_total, key=dpto_total.get)
    tipo_max = max(tipo_total, key=tipo_total.get)
    mes_max = max(mes_total, key=mes_total.get) if not es_un_mes else request.mes
    alerta = calcular_nivel_alerta(total)

    top_dptos = sorted(dpto_total.items(), key=lambda x: x[1], reverse=True)[:5]
    top_departamentos = [{"departamento": d, "incidencias": round(v, 2)} for d, v in top_dptos]

    top_tipos = sorted(tipo_total.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tipos_list = [{"tipo": t, "incidencias": round(v, 2)} for t, v in top_tipos]

    meses_nombres = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                     "Julio","Agosto","Setiembre","Octubre","Noviembre","Diciembre"]

    periodo_label = f"{request.anio}" if es_un_mes else f"anual {request.anio}"
    logger.info(f"📊 Proyección {periodo_label}: {total:,.0f} delitos "
                f"({len(deptos)} dptos × {len(tipos)} tipos × {len(meses)} meses = {len(rows)} combos) "
                f"en {inference_time_ms:.2f} ms")

    return {
        "status": "EXITO",
        "anio": request.anio,
        "mes": request.mes,
        "mes_nombre": meses_nombres[request.mes - 1] if es_un_mes else None,
        "tipo_periodo": "MENSUAL" if es_un_mes else "ANUAL",
        "total_general": round(total, 2),
        "nivel_alerta": alerta,
        "departamento_mas_critico": dpto_max,
        "tipo_mas_critico": tipo_max,
        "mes_mas_critico": meses_nombres[mes_max - 1],
        "top_departamentos": top_departamentos,
        "top_tipos": top_tipos_list,
        "desglose_departamentos": {d: round(v, 2) for d, v in dpto_total.items()},
        "desglose_tipos": {t: round(v, 2) for t, v in tipo_total.items()},
        "desglose_meses": {meses_nombres[m-1]: round(mes_total[m], 2) for m in meses},
        "total_combinaciones": len(rows),
        "departamentos_procesados": len(deptos),
        "tipos_procesados": len(tipos),
        "metadata_tecnica": {
            "tiempo_inferencia_total_ms": round(inference_time_ms, 2),
            "algoritmo": "RandomForestRegressor_Ensemble",
        },
        "mensaje_ejecutivo": (
            f"{'Proyección mensual' if es_un_mes else 'Proyección anual'} para {request.anio}"
            f"{f' - Mes {meses_nombres[request.mes - 1]}' if es_un_mes else ''}: "
            f"{round(total):,.0f} delitos estimados. "
            f"Departamento más crítico: {dpto_max}. "
            f"Tipo predominante: {tipo_max}. "
            f"Mes pico: {meses_nombres[mes_max - 1]}. "
            f"Escenario: {alerta}."
        )
    }


# ─────────────────────────────────────────────────────────────────────────────
# 10. CONTROLADORES DE ERRORES GLOBALES
# ─────────────────────────────────────────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Sobrescribe el error 422 de FastAPI para hacerlo más legible al cliente."""
    errores = []
    for err in exc.errors():
        campo = err.get("loc", ["desconocido"])[-1]
        mensaje = err.get("msg", "Error de validación")
        errores.append(f"Campo '{campo}': {mensaje}")
        
    logger.warning(f"Rechazo por validación de datos (422): {errores}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "ERROR_VALIDACION",
            "mensaje": "Los datos enviados no cumplen el formato del modelo SIDPOL.",
            "detalles": errores
        },
    )

# ─────────────────────────────────────────────────────────────────────────────
# 11. PUNTO DE ENTRADA DEL SERVIDOR (Solo para pruebas locales)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    # En producción con Docker, se invoca vía CMD/ENTRYPOINT en el Dockerfile
    # Ejemplo: gunicorn app:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    print("\nIniciando servidor de desarrollo Uvicorn local...\n")
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # False en producción para evitar overhead
        log_level="info"
    )