"""
================================================================================
🧠 MOTOR PREDICTIVO SIDPOL - ENTRENAMIENTO SUPERVISADO Y BALANCEO ESTRATÉGICO
================================================================================
Proyecto    : Sistema Inteligente de Predicción de Incidencia Delictiva (SIDPOL)
Metodología : CRISP-DM (Cross Industry Standard Process for Data Mining)
Autores     : Jhon Ordoñez, Luis Angeles, Angel Leon, Jean Loa — UTP
Dataset     : Base_datos_SIDPOL_Marzo2026.xlsx | 6,510 registros

Descripción :
Este script de nivel de producción orquesta el pipeline de Machine Learning 
para predecir la criminalidad departamental. Incluye:
  1. Carga y validación robusta de datos.
  2. Análisis Exploratorio de Datos (EDA) con múltiples visualizaciones.
  3. Preprocesamiento avanzado (OneHotEncoding) y balanceo sintético (SMOTE).
  4. Búsqueda de hiperparámetros (GridSearchCV) para Random Forest.
  5. Evaluación comparativa contra un modelo base (Regresión Lineal).
  6. Exportación del artefacto (.pkl) para consumo vía FastAPI.

Versión     : 4.0.0 (Enterprise Edition)
================================================================================
"""

import sys
import time
import json
import logging
import warnings
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger = logging.getLogger("SIDPOL.Core")
    logger.warning("plotly no instalado. Se omitirá exportación de gráficos Plotly.")

# ------------------------------------------------------------------------------
# CONFIGURACIÓN DEL ENTORNO
# ------------------------------------------------------------------------------
warnings.filterwarnings("ignore")
try:
    matplotlib.use("TkAgg")  # Óptimo para Linux/KDE Plasma
except Exception:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SIDPOL.Core")

# ------------------------------------------------------------------------------
# CLASES DE EXCEPCIÓN PERSONALIZADAS
# ------------------------------------------------------------------------------
class SIDPOLBaseException(Exception):
    """Clase base para excepciones del sistema SIDPOL."""
    pass

class SIDPOLDataError(SIDPOLBaseException):
    """Excepción lanzada cuando hay inconsistencias críticas en el dataset."""
    pass

class SIDPOLModelError(SIDPOLBaseException):
    """Excepción lanzada cuando falla el entrenamiento o balanceo."""
    pass

# ------------------------------------------------------------------------------
# CONFIGURACIONES Y CONSTANTES (DATACLASSES)
# ------------------------------------------------------------------------------
@dataclass
class SIDPOLConfig:
    """Almacena la configuración global del sistema y rutas de archivos."""
    ruta_excel: Path = Path(__file__).parent / "Base_datos_SIDPOL_Marzo2026.xlsx"
    hoja_excel: str = "Temp2"
    ruta_modelo_salida: Path = Path(__file__).parent / "pipeline_sidpol.pkl"
    random_state: int = 42
    test_size: float = 0.20
    anio_inicio: int = 2018
    anio_fin: int = 2026

@dataclass
class FeaturesConfig:
    """Define la estructura y nombres de las características (features)."""
    col_anio: str = "anio"
    col_mes: str = "mes"
    col_dpto: str = "dpto_hecho_new"
    col_delito: str = "es_delito_x"
    col_target: str = "total_delitos"
    
    @property
    def categoricas(self) -> List[str]:
        return [self.col_dpto, self.col_delito]
    
    @property
    def numericas(self) -> List[str]:
        return [self.col_anio, self.col_mes]
    
    @property
    def todas_predictoras(self) -> List[str]:
        return self.numericas + self.categoricas

# Instancias globales de configuración
config = SIDPOLConfig()
features = FeaturesConfig()

# ------------------------------------------------------------------------------
# FASE 1: CARGA Y LIMPIEZA DE DATOS
# ------------------------------------------------------------------------------
class DataLoader:
    """Responsable de la extracción, filtrado y limpieza del dataset SIDPOL."""
    
    def __init__(self, cfg: SIDPOLConfig, f_cfg: FeaturesConfig):
        self.cfg = cfg
        self.f = f_cfg
        
    def ejecutar_pipeline_carga(self) -> pd.DataFrame:
        """Orquesta la lectura y limpieza de datos."""
        logger.info("Iniciando Fase 1: Carga y Comprensión de Datos...")
        df = self._leer_excel()
        df = self._estandarizar_columnas(df)
        df = self._filtrar_temporalidad(df)
        df = self._renombrar_target(df)
        df = self._imputar_nulos(df)
        self._validar_integridad(df)
        logger.info(f"Fase 1 completada. Dataset final: {df.shape[0]} filas x {df.shape[1]} columnas.")
        return df

    def _leer_excel(self) -> pd.DataFrame:
        if not self.cfg.ruta_excel.exists():
            raise SIDPOLDataError(f"El archivo no existe en la ruta: {self.cfg.ruta_excel}")
        
        try:
            logger.info(f"Leyendo hoja '{self.cfg.hoja_excel}' de {self.cfg.ruta_excel.name}...")
            return pd.read_excel(self.cfg.ruta_excel, sheet_name=self.cfg.hoja_excel)
        except ValueError:
            logger.warning(f"La hoja '{self.cfg.hoja_excel}' no existe. Cargando primera hoja disponible.")
            return pd.read_excel(self.cfg.ruta_excel, sheet_name=0)
            
    def _estandarizar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convierte todas las cabeceras a minúsculas sin espacios extra."""
        df.columns = df.columns.str.strip().str.lower()
        return df
        
    def _filtrar_temporalidad(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica el filtro de años definido en la investigación."""
        if self.f.col_anio not in df.columns:
            raise SIDPOLDataError(f"Falta la columna temporal: '{self.f.col_anio}'")
            
        df[self.f.col_anio] = pd.to_numeric(df[self.f.col_anio], errors='coerce')
        df_filtrado = df[(df[self.f.col_anio] >= self.cfg.anio_inicio) & 
                         (df[self.f.col_anio] <= self.cfg.anio_fin)].copy()
        logger.info(f"Filtrado por años ({self.cfg.anio_inicio}-{self.cfg.anio_fin}). Registros: {len(df_filtrado)}")
        return df_filtrado

    def _renombrar_target(self, df: pd.DataFrame) -> pd.DataFrame:
        """Garantiza que la variable objetivo tenga el nombre correcto."""
        if 'n_dist_id_dgc' in df.columns:
            df.rename(columns={'n_dist_id_dgc': self.f.col_target}, inplace=True)
        elif self.f.col_target not in df.columns:
            raise SIDPOLDataError("No se encontró la variable objetivo de delitos.")
        return df

    def _imputar_nulos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rellena valores nulos utilizando heurísticas estadísticas."""
        nulos_iniciales = df.isnull().sum().sum()
        if nulos_iniciales > 0:
            logger.warning(f"Detectados {nulos_iniciales} valores nulos. Procediendo a imputación...")
            
            # Numéricas se rellenan con 0
            cols_num = df.select_dtypes(include=[np.number]).columns
            df[cols_num] = df[cols_num].fillna(0)
            
            # Categóricas se rellenan con la moda (el valor más frecuente)
            for col in self.f.categoricas:
                if col in df.columns and df[col].isnull().any():
                    moda_val = df[col].mode()[0]
                    df[col].fillna(moda_val, inplace=True)
                    
            logger.info("Imputación de nulos finalizada.")
        return df

    def _validar_integridad(self, df: pd.DataFrame) -> None:
        """Verifica que todas las columnas necesarias existan."""
        cols_requeridas = self.f.todas_predictoras + [self.f.col_target]
        faltantes = [c for c in cols_requeridas if c not in df.columns]
        if faltantes:
            raise SIDPOLDataError(f"Faltan columnas críticas en el dataset: {faltantes}")

# ------------------------------------------------------------------------------
# FASE 2: ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# ------------------------------------------------------------------------------
class VisualizadorEDA:
    """Genera reportes visuales estadísticos para comprender la distribución del delito."""
    
    def __init__(self, f_cfg: FeaturesConfig):
        self.f = f_cfg

    def generar_dashboard_visual(self, df: pd.DataFrame) -> None:
        """Orquesta la creación de múltiples gráficos en ventanas separadas."""
        logger.info("Iniciando Fase 2: Análisis Exploratorio de Datos (EDA)...")
        logger.info("ATENCIÓN: Se abrirán ventanas gráficas. CIÉRRELAS para continuar con el entrenamiento.")
        
        sns.set_theme(style="whitegrid")
        total_delitos = df[self.f.col_target].sum()
        
        self._plot_por_departamento(df, total_delitos)
        self._plot_por_tipo_delito(df, total_delitos)
        self._plot_tendencia_anual(df)
        
        plt.show()

    def _plot_por_departamento(self, df: pd.DataFrame, total: float) -> None:
        """Gráfico de barras horizontales: Incidencia por Departamento."""
        dpto_df = df.groupby(self.f.col_dpto)[self.f.col_target].sum().reset_index()
        dpto_df['porcentaje'] = (dpto_df[self.f.col_target] / total) * 100
        dpto_df = dpto_df.sort_values(by='porcentaje', ascending=True)

        plt.figure("SIDPOL - Análisis por Departamento", figsize=(12, 8))
        ax = sns.barplot(x='porcentaje', y=self.f.col_dpto, data=dpto_df, palette='Blues_d')
        
        plt.title('Distribución de la Incidencia Delictiva por Departamento', fontsize=14, pad=15)
        plt.xlabel('Porcentaje del Total Nacional (%)', fontsize=12)
        plt.ylabel('Departamento', fontsize=12)
        
        # Añadir etiquetas a las barras
        for p in ax.patches:
            width = p.get_width()
            plt.text(width + 0.3, p.get_y() + p.get_height()/2. + 0.1, 
                     f'{width:.1f}%', ha="left", fontsize=9)
        plt.tight_layout()

    def _plot_por_tipo_delito(self, df: pd.DataFrame, total: float) -> None:
        """Gráfico de barras: Frecuencia de tipos de delitos."""
        tipo_df = df.groupby(self.f.col_delito)[self.f.col_target].sum().reset_index()
        tipo_df['porcentaje'] = (tipo_df[self.f.col_target] / total) * 100
        tipo_df = tipo_df.sort_values(by='porcentaje', ascending=True)

        plt.figure("SIDPOL - Análisis por Tipo de Delito", figsize=(10, 6))
        ax = sns.barplot(x='porcentaje', y=self.f.col_delito, data=tipo_df, palette='Oranges_r')
        
        plt.title('Prevalencia por Tipo de Clasificación Delictiva', fontsize=14, pad=15)
        plt.xlabel('Porcentaje (%)', fontsize=12)
        plt.ylabel('Clasificación', fontsize=12)
        plt.tight_layout()

    def _plot_tendencia_anual(self, df: pd.DataFrame) -> None:
        """Gráfico de líneas: Tendencia del delito a lo largo de los años."""
        tendencia = df.groupby(self.f.col_anio)[self.f.col_target].sum().reset_index()
        
        plt.figure("SIDPOL - Tendencia Temporal", figsize=(8, 5))
        sns.lineplot(x=self.f.col_anio, y=self.f.col_target, data=tendencia, 
                     marker='o', color='red', linewidth=2.5, markersize=8)
        
        plt.title('Evolución Histórica Total de Delitos (2022 - 2026)', fontsize=14, pad=15)
        plt.xlabel('Año', fontsize=12)
        plt.ylabel('Volumen Total de Delitos', fontsize=12)
        plt.xticks(tendencia[self.f.col_anio]) 
        plt.tight_layout()

# ------------------------------------------------------------------------------
# FASE 3: PREPROCESAMIENTO Y FAIRNESS (SMOTE)
# ------------------------------------------------------------------------------
class IngenieriaCaracteristicas:
    """Maneja el encoding, división de datos y el balanceo sintético SMOTE."""
    
    def __init__(self, cfg: SIDPOLConfig, f_cfg: FeaturesConfig):
        self.cfg = cfg
        self.f = f_cfg
        self.preprocessor = None

    def crear_preprocesador(self) -> ColumnTransformer:
        """Configura el OneHotEncoder para transformar texto a matrices matemáticas."""
        logger.info("Configurando Transformadores de Columnas (OneHotEncoder)...")
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), self.f.categoricas)
            ],
            remainder='passthrough'
        )
        return self.preprocessor

    def preparar_datos(self, df: pd.DataFrame) -> Tuple:
        """Split temporal, log-transform del target, encoding. Sin SMOTE."""
        logger.info("Iniciando Fase 3: Ingeniería de Features con split temporal...")

        X = df[self.f.todas_predictoras]
        y = df[self.f.col_target]

        # 1. Ordenar por año para split temporal limpio
        df_sorted = df.sort_values(self.f.col_anio)
        X_sorted = df_sorted[self.f.todas_predictoras]
        y_sorted = df_sorted[self.f.col_target]

        split_idx = int(len(df_sorted) * (1 - self.cfg.test_size))
        X_train = X_sorted.iloc[:split_idx]
        X_test  = X_sorted.iloc[split_idx:]
        y_train_raw = y_sorted.iloc[:split_idx]
        y_test_raw  = y_sorted.iloc[split_idx:]

        logger.info(f"Split temporal -> Train: {len(X_train)} (años {X_train[self.f.col_anio].min()}-{X_train[self.f.col_anio].max()}) "
                     f"| Test: {len(X_test)} (años {X_test[self.f.col_anio].min()}-{X_test[self.f.col_anio].max()})")

        # 2. Log-transform del target (corrige cola pesada: mean=614 vs median=133)
        y_train = np.log1p(y_train_raw)
        y_test  = np.log1p(y_test_raw)
        logger.info(f"Log-transform aplicado. Target raw: skew={y_train_raw.skew():.2f} | log: skew={pd.Series(y_train).skew():.2f}")

        # 3. Transformación categórica (OneHotEncoder)
        self.crear_preprocesador()
        X_train_encoded = self.preprocessor.fit_transform(X_train)

        logger.info(f"Encoding completado. Features generadas: {X_train_encoded.shape[1]}")
        return X_train_encoded, X_test, y_train, y_test

# ------------------------------------------------------------------------------
# FASE 4: ENTRENAMIENTO, HIPERPARÁMETROS Y EVALUACIÓN
# ------------------------------------------------------------------------------
class ModelTrainer:
    """Encargado de entrenar modelos, buscar los mejores parámetros y extraer métricas."""
    
    def __init__(self, preprocessor: ColumnTransformer, cfg: SIDPOLConfig):
        self.preprocessor = preprocessor
        self.cfg = cfg
        self.mejor_modelo_rf = None

    def _calcular_mape(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calcula el Error Porcentual Absoluto Medio (evitando división por cero)."""
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        mask = y_true != 0
        if not mask.any():
            return 0.0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    def imprimir_metricas(self, nombre: str, y_true: pd.Series, y_pred: np.ndarray) -> None:
        """Formatea e imprime un reporte estadístico riguroso."""
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = self._calcular_mape(y_true, y_pred)
        
        print(f"\n{'='*40}")
        print(f" 🏆 RESULTADOS: {nombre.upper()} ")
        print(f"{'='*40}")
        print(f" • R² Score (Varianza explicada) : {r2:.4f}")
        print(f" • MAE (Error Absoluto Medio)    : {mae:.2f} delitos")
        print(f" • RMSE (Raíz Error Cuadrático)  : {rmse:.2f} delitos")
        print(f" • MAPE (Error Porcentual)       : {mape:.2f} %")
        print(f"{'='*40}")

    def entrenar_baseline_lineal(self, X_train, y_train, X_test, y_test) -> None:
        """Entrena el modelo de Regresión Lineal como base de comparación."""
        logger.info("Entrenando Modelo Baseline: Regresión Lineal Múltiple...")
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        
        # Transformar el set de prueba antes de predecir
        X_test_encoded = self.preprocessor.transform(X_test)
        y_pred = lr_model.predict(X_test_encoded)
        
        self.imprimir_metricas("Regresión Lineal", y_test, y_pred)

    def entrenar_random_forest_optimizado(self, X_train, y_train, X_test, y_test) -> ImbPipeline:
        """
        Entrena el Random Forest utilizando GridSearchCV para encontrar
        los mejores hiperparámetros de manera automatizada.
        """
        logger.info("Iniciando Búsqueda de Hiperparámetros (GridSearchCV) para Random Forest...")
        
        # Definición del espacio de búsqueda (Hyperparameter Grid)
        param_distributions = {
            'n_estimators': [100, 200, 300, 500],
            'max_depth': [None, 10, 20, 30, 40],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', 1.0]
        }
        
        rf_base = RandomForestRegressor(random_state=self.cfg.random_state, n_jobs=-1)
        
        # K-Fold Cross Validation
        cv_fold = KFold(n_splits=3, shuffle=True, random_state=self.cfg.random_state)
        
        random_search = RandomizedSearchCV(
            estimator=rf_base,
            param_distributions=param_distributions,
            n_iter=30,
            cv=cv_fold,
            scoring='r2',
            verbose=1,
            n_jobs=-1,
            random_state=self.cfg.random_state
        )
        
        tiempo_inicio = time.time()
        random_search.fit(X_train, y_train)
        tiempo_fin = time.time()
        
        self.mejor_modelo_rf = random_search.best_estimator_
        logger.info(f"Optimización completada en {tiempo_fin - tiempo_inicio:.2f} segundos.")
        logger.info(f"Mejores Parámetros encontrados: {random_search.best_params_}")
        
        # Evaluación Final en el Test Set
        X_test_encoded = self.preprocessor.transform(X_test)
        y_pred_rf = self.mejor_modelo_rf.predict(X_test_encoded)
        
        self.imprimir_metricas("Random Forest Regressor (Optimizado)", y_test, y_pred_rf)
        self._analizar_importancia_variables()
        
        # Construir y retornar el Pipeline definitivo listo para producción
        return ImbPipeline(steps=[
            ('preprocesador', self.preprocessor),
            ('modelo_rf', self.mejor_modelo_rf)
        ])

    def _analizar_importancia_variables(self) -> None:
        """Extrae e imprime las características matemáticas que más influyen en el delito."""
        if self.mejor_modelo_rf is None:
            return
            
        logger.info("Extrayendo Importancia de Variables (Feature Importance)...")
        importancias = self.mejor_modelo_rf.feature_importances_
        nombres_features = self.preprocessor.get_feature_names_out()
        
        # Agrupar importancias en un DataFrame
        df_imp = pd.DataFrame({
            'Feature': nombres_features,
            'Importancia': importancias
        }).sort_values(by='Importancia', ascending=False).head(5)
        
        print("\n--- TOP 5 VARIABLES MÁS INFLUYENTES ---")
        for idx, row in df_imp.iterrows():
            nombre_limpio = row['Feature'].replace("cat__", "").replace("remainder__", "")
            print(f"  {nombre_limpio:<30} : {row['Importancia']:.4f}")
        print("---------------------------------------")

# ------------------------------------------------------------------------------
# FASE 5: EXPORTACIÓN Y DESPLIEGUE
# ------------------------------------------------------------------------------
class ExportadorModelo:
    """Serializa el pipeline de ML para su consumo en la API de FastAPI."""
    
    @staticmethod
    def guardar_pipeline(pipeline: ImbPipeline, ruta: Path) -> None:
        logger.info(f"Iniciando Fase 5: Serialización y Exportación...")
        try:
            joblib.dump(pipeline, ruta, compress=3) # Compresión óptima para Docker
            tamano_mb = ruta.stat().st_size / (1024 * 1024)
            logger.info(f"✅ EXITO: Pipeline exportado correctamente en: {ruta.resolve()}")
            logger.info(f"   Peso del artefacto: {tamano_mb:.2f} MB")
            logger.info("   El contenedor FastAPI ya puede cargar 'pipeline_sidpol.pkl' para inferencia en tiempo real.")
        except Exception as e:
            raise SIDPOLModelError(f"Error crítico al intentar guardar el modelo: {e}")

class ExportadorMetricas:
    """Persiste las métricas de evaluación y los gráficos Plotly como JSON."""
    
    @staticmethod
    def guardar_metricas(metricas: Dict[str, Any], ruta: Path) -> None:
        logger.info("Persistiendo métricas del modelo como JSON...")
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(metricas, f, indent=2, ensure_ascii=False, default=str)
            tamano_kb = ruta.stat().st_size / 1024
            logger.info(f"✅ Métricas exportadas en: {ruta.resolve()} ({tamano_kb:.2f} KB)")
        except Exception as e:
            logger.error(f"No se pudo guardar el archivo de métricas: {e}")

    @staticmethod
    def construir_metricas(
        model_trainer: ModelTrainer,
        y_test: pd.Series,
        y_pred: np.ndarray,
        df_limpio: pd.DataFrame,
        f_cfg: FeaturesConfig
    ) -> Dict[str, Any]:
        r2 = float(r2_score(y_test, y_pred))
        mae = float(mean_absolute_error(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mape = float(model_trainer._calcular_mape(y_test, y_pred))

        metricas = {
            "resumen": {
                "r2_score": round(r2, 4),
                "mae": round(mae, 2),
                "rmse": round(rmse, 2),
                "mape": round(mape, 2),
                "algoritmo": "RandomForestRegressor",
                "best_params": model_trainer.mejor_modelo_rf.get_params()
                if model_trainer.mejor_modelo_rf else {}
            },
            "importancia_variables": {},
            "data_metrics": {
                "total_registros": len(df_limpio),
                "total_delitos": int(df_limpio[f_cfg.col_target].sum()),
                "promedio_delitos": float(round(df_limpio[f_cfg.col_target].mean(), 2))
            }
        }

        if model_trainer.mejor_modelo_rf is not None:
            importancias = model_trainer.mejor_modelo_rf.feature_importances_
            nombres = model_trainer.preprocessor.get_feature_names_out()
            for nombre, imp in zip(nombres, importancias):
                nombre_limpio = nombre.replace("cat__", "").replace("remainder__", "")
                metricas["importancia_variables"][nombre_limpio] = round(float(imp), 4)

        return metricas

    @staticmethod
    def generar_graficos_plotly(
        df: pd.DataFrame,
        f_cfg: FeaturesConfig,
        ruta_salida: Path
    ) -> None:
        if not PLOTLY_AVAILABLE:
            logger.warning("Plotly no disponible. No se generarán gráficos JSON.")
            return

        logger.info("Generando gráficos Plotly en formato JSON para Angular...")
        total = df[f_cfg.col_target].sum()
        graficos = {}

        dpto_df = df.groupby(f_cfg.col_dpto)[f_cfg.col_target].sum().reset_index()
        dpto_df['porcentaje'] = (dpto_df[f_cfg.col_target] / total) * 100
        dpto_df = dpto_df.sort_values('porcentaje', ascending=True)
        fig_dpto = go.Figure([go.Bar(
            x=dpto_df['porcentaje'],
            y=dpto_df[f_cfg.col_dpto],
            orientation='h',
            marker_color='#1f77b4'
        )])
        fig_dpto.update_layout(
            title='Incidencia Delictiva por Departamento',
            xaxis_title='Porcentaje del Total Nacional (%)',
            yaxis_title='Departamento',
            height=500
        )
        graficos["por_departamento"] = json.loads(fig_dpto.to_json())

        tipo_df = df.groupby(f_cfg.col_delito)[f_cfg.col_target].sum().reset_index()
        tipo_df['porcentaje'] = (tipo_df[f_cfg.col_target] / total) * 100
        tipo_df = tipo_df.sort_values('porcentaje', ascending=True)
        fig_tipo = go.Figure([go.Bar(
            x=tipo_df['porcentaje'],
            y=tipo_df[f_cfg.col_delito],
            orientation='h',
            marker_color='#ff7f0e'
        )])
        fig_tipo.update_layout(
            title='Prevalencia por Tipo de Clasificación Delictiva',
            xaxis_title='Porcentaje (%)',
            yaxis_title='Clasificación',
            height=400
        )
        graficos["por_tipo_delito"] = json.loads(fig_tipo.to_json())

        tendencia = df.groupby(f_cfg.col_anio)[f_cfg.col_target].sum().reset_index()
        fig_tend = go.Figure([go.Scatter(
            x=tendencia[f_cfg.col_anio],
            y=tendencia[f_cfg.col_target],
            mode='lines+markers',
            marker=dict(color='red', size=8),
            line=dict(width=2.5)
        )])
        fig_tend.update_layout(
            title='Evolución Histórica Total de Delitos',
            xaxis_title='Año',
            yaxis_title='Volumen Total de Delitos',
            height=400
        )
        graficos["tendencia_anual"] = json.loads(fig_tend.to_json())

        try:
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                json.dump(graficos, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Gráficos Plotly exportados en: {ruta_salida.resolve()}")
        except Exception as e:
            logger.error(f"Error al exportar gráficos Plotly: {e}")

# ------------------------------------------------------------------------------
# ORQUESTADOR PRINCIPAL (MAIN)
# ------------------------------------------------------------------------------
def main():
    """Función de punto de entrada que ejecuta el ciclo CRISP-DM completo."""
    print("\n" + "*" * 70)
    print(" 🛡️  S.I.D.P.O.L. - MOTOR DE INTELIGENCIA ARTIFICIAL (V4.0 Enterprise) 🛡️")
    print("*" * 70 + "\n")
    
    try:
        # 1. Carga de Datos
        cargador = DataLoader(config, features)
        df_limpio = cargador.ejecutar_pipeline_carga()
        
        # 2. Análisis Exploratorio (EDA) — omitido en modo entrenamiento automático
        # eda = VisualizadorEDA(features)
        # eda.generar_dashboard_visual(df_limpio)
        logger.info("Fase 2 (EDA) omitida — modo entrenamiento silencioso.")
        
        # 3. Ingeniería (split temporal + log-target, sin SMOTE)
        ingenieria = IngenieriaCaracteristicas(config, features)
        X_train_enc, X_test, y_train_log, y_test_log = ingenieria.preparar_datos(df_limpio)
        
        # 4. Entrenamiento y Evaluación
        entrenador = ModelTrainer(ingenieria.preprocessor, config)
        
        # 4.1 Entrenar Base de Comparación
        entrenador.entrenar_baseline_lineal(X_train_enc, y_train_log, X_test, y_test_log)
        
        # 4.2 Entrenar Modelo Avanzado (Random Forest con Tuning)
        pipeline_final = entrenador.entrenar_random_forest_optimizado(
            X_train_enc, y_train_log, X_test, y_test_log
        )
        
        # 5. Evaluación final en Test (inverse log-transform para métricas en escala real)
        X_test_encoded = ingenieria.preprocessor.transform(X_test)
        y_pred_log = entrenador.mejor_modelo_rf.predict(X_test_encoded)
        y_pred_final = np.expm1(y_pred_log)  # volver a escala original
        y_test_original = np.expm1(y_test_log)

        # 6. Exportación del pipeline
        ExportadorModelo.guardar_pipeline(pipeline_final, config.ruta_modelo_salida)

        # 7. Exportación de métricas y gráficos
        metricas = ExportadorMetricas.construir_metricas(
            entrenador, y_test_original, y_pred_final, df_limpio, features
        )
        ruta_metricas = config.ruta_modelo_salida.parent / "metricas_sidpol.json"
        ExportadorMetricas.guardar_metricas(metricas, ruta_metricas)

        ruta_graficos = config.ruta_modelo_salida.parent / "graficos_sidpol.json"
        ExportadorMetricas.generar_graficos_plotly(df_limpio, features, ruta_graficos)
        
    except SIDPOLBaseException as e:
        logger.error(f"Error Controlado en SIDPOL: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Error Inesperado del Sistema: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()