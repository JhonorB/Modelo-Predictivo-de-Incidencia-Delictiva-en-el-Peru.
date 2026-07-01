`# 🏛️ Arquitectura y Metodología del Sistema SIDPOL

Este documento detalla la arquitectura empresarial y la base metodológica del Sistema Inteligente de Predicción de Incidencia Delictiva (SIDPOL). 

---

## 1. Fundamento Metodológico y Científico

### Metodología CRISP-DM
El proyecto se desarrolla bajo el estándar industrial CRISP-DM (Cross-Industry Standard Process for Data Mining), estructurado en 6 fases secuenciales:

1.  **Comprensión del Negocio:** Identificación del reto de seguridad ciudadana en el Perú y la necesidad de pasar de un enfoque reactivo a uno proactivo[cite: 5].
2.  **Comprensión de los Datos:** Análisis de los 6,510 registros oficiales del SIDPOL correspondientes al periodo 2022–2026[cite: 5].
3.  **Preparación de los Datos:** Preprocesamiento en Python utilizando Pandas y NumPy, incluyendo limpieza, normalización y aplicación de la técnica SMOTE para corregir el desbalance regional[cite: 5].
4.  **Modelado:** Implementación de algoritmos predictivos a través de la librería Scikit-Learn[cite: 5].
5.  **Evaluación:** Medición del rendimiento de los algoritmos (Random Forest Regressor vs. Regresión Lineal) mediante métricas estadísticas (R² Score, Mean Absolute Error (MAE) y Root Mean Squared Error (RMSE))[cite: 5].
6.  **Despliegue:** Integración del modelo en una arquitectura de microservicios web de alta disponibilidad mediante contenedores Docker[cite: 5].

### Enfoque de Inteligencia Artificial: Machine Learning Supervisado
El sistema utiliza exclusivamente **Machine Learning Supervisado**. 
Se define como el paradigma mediante el cual los modelos aprenden funciones predictivas a partir de datos históricos previamente etiquetados[cite: 5]. En este contexto:
*   **Las variables predictoras (X):** Año, Mes, Departamento y Tipo de Delito.
*   **La variable objetivo o etiqueta (y):** El total de delitos cometidos.
Al proporcionarle a la máquina ejemplos del pasado donde ya conocemos el resultado exacto, el modelo aprende los patrones matemáticos y puede generalizarlos para calcular proyecciones precisas hacia información nueva[cite: 5]. (Se descarta el aprendizaje *No Supervisado*, ya que el objetivo no es agrupar datos desconocidos, sino predecir una variable numérica concreta mediante Regresión).

---

## 2. Componentes Principales de la Arquitectura

El sistema utiliza un patrón de **Microservicios Híbridos**, dividido en tres grandes bloques y orquestado mediante contenedores:

### A. Frontend (Capa de Presentación)
*   **Tecnología:** Angular 19 + SCSS.
*   **UI/UX:** Angular Material, diseño tipo SaaS corporativo (modo claro/oscuro).
*   **Módulos:** Login, Dashboard Ejecutivo (KPIs), Historial y Panel de Predicciones.
*   **Directorio:** `sidpol-frontend/`

### B. Backend (Capa Lógica Core)
*   **Tecnología:** Java 21 + Spring Boot 3.
*   **Seguridad:** Spring Security + JWT (JSON Web Tokens) para autenticación de roles.
*   **Persistencia (Datos de la App):** Spring Data JPA conectado al servicio MySQL Dockerizado (`db-sidpol`). Aquí se guardan los usuarios, credenciales, roles y el historial de auditoría.
*   **Directorio:** `sidpol-backend/`

### C. Inteligencia Artificial (Capa Predictiva Dockerizada)
*   **Tecnología:** Python 3.11-slim (Pandas, Scikit-Learn, FastAPI, Uvicorn).
*   **Infraestructura:** Desplegado en un contenedor Docker (`motor_ia`) para evitar bloqueos del sistema de archivos local y conflictos de dependencias. Expuesto en el puerto 8000.
*   **Función:** Recibe parámetros vía HTTP POST (JSON), carga el modelo predictivo (Random Forest) en memoria mediante el ciclo de vida de la app y devuelve la proyección estimada de incidencia delictiva.
*   **Directorio:** `motor_Sidpol/`

---

## 3. Entorno de Despliegue y Orquestación (Docker)

Para garantizar la reproducibilidad y agilidad en el desarrollo, la base de datos y la capa de IA se gestionan mediante **Docker Compose**. 

El archivo unificado de orquestación define dos servicios principales:
1. **`db-sidpol`**: Contenedor basado en la imagen oficial de `mysql:8.0`. Se encarga de la persistencia transaccional del backend Spring Boot.
2. **`motor_ia`**: Contenedor basado en `python:3.11-slim` que construye la imagen del microservicio de Machine Learning, exponiendo FastAPI para consultas.

---

## 4. Estructura de Directorios del Proyecto

```text
DATA_PROYEC/
│
├── sidpol-frontend/             # 🌐 Interfaz de Usuario
│
├── sidpol-backend/              # ⚙️ Orquestador y Seguridad (Spring Boot)
│
└── motor_Sidpol/                # 🧠 Microservicio IA Dockerizado (Python)
    ├── docker-compose.yml       # 🐳 Orquestación (db-sidpol + motor_ia)
    ├── Dockerfile               # 🐳 Receta de construcción de la API en Python
    ├── Base_datos_SIDPOL_Marzo2026.xlsx  # 📊 Datos crudos de entrenamiento
    ├── app.py                   # Servidor API FastAPI
    ├── script_modelo_sidpol.py  # Script de entrenamiento y SMOTE
    ├── rf_model.pkl             # Modelo entrenado listo para inferir
    └── requirements.txt         # Dependencias de Python
```

---

## 5. Prerrequisitos y Guía de Instalación

### Prerrequisitos
*   Tener **Docker Desktop** o el motor de Docker instalado y ejecutándose.
*   Tener Java 21 y Maven instalados (para el backend).
*   Tener Node.js instalado (para el frontend).

### Levantar el Entorno Backend y Base de Datos

Gracias a la dockerización, puedes inicializar tanto el motor predictivo de Inteligencia Artificial (FastAPI) como la base de datos MySQL transaccional con un solo comando.

1. Abre una terminal y navega hasta el directorio del motor de IA:
   ```bash
   cd motor_Sidpol
   ```
2. Ejecuta el siguiente comando para construir las imágenes y levantar los servicios en segundo plano:
   ```bash
   docker compose up --build -d
   ```
3. **Verificación:** 
   * La Base de Datos MySQL estará disponible en el puerto `3306`.
   * La API Predictiva de Python estará disponible en: `http://localhost:8000/api/v1/health`.

Una vez que los contenedores estén corriendo (`db-sidpol` y `motor_ia`), puedes iniciar independientemente tu aplicación en **Spring Boot** (que se conectará a estos puertos) y tu **Frontend**.`