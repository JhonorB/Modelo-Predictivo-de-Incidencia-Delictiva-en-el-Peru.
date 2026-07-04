# Plan FINAL — Reorganización Narrativa + Formato del Artículo SIDPOL

## Estado: Listo para implementar

Basado en la retroalimentación completa del autor.
No se modifican: modelo, dataset, arquitectura, metodología CRISP-DM ni métricas.

---

## 1. Cambio narrativo central

| ❌ Viejo enfoque | ✅ Nuevo enfoque |
|------------------|-----------------|
| Predicción de criminalidad | **Pronóstico de denuncias** |
| Predictive Policing | **Decision Support System (DSS)** |
| Anticipar delitos | **Planificación estratégica de recursos** |
| Prevenir crimen con IA | **Toma de decisiones basada en datos** |
| Identificar delincuentes/zonas de riesgo | **Gestión pública y transformación digital** |

### Vocabulario específico: buscar y reemplazar en todo el artículo

| Buscar (textos actuales) | Reemplazar por |
|--------------------------|----------------|
| predecir criminalidad | pronosticar denuncias |
| anticipar delitos | estimar demanda de atención policial |
| prevenir delitos | apoyar la planificación estratégica |
| seguridad proactiva | gestión basada en datos |
| predicción del delito | pronóstico de denuncias delictivas |
| actuar antes del crimen | asignar recursos institucionales |
| predictive policing | sistema de apoyo a decisiones (DSS) |

---

## 2. Título definitivo

> **Modelo de pronóstico de denuncias delictivas mediante aprendizaje supervisado para apoyar la planificación estratégica de la seguridad ciudadana en el Perú utilizando datos del SIDPOL (2022–2026).**

---

## 3. Estructura final del artículo

```
ARTICLE INFO (tabla 2 cols)
TÍTULO
Autores + afiliación

RESUMEN (narrativa DSS)
Palabras clave (bullets)

ABSTRACT (inglés)
Keywords (bullets)

I. INTRODUCCIÓN
   - Justificación: planificación estratégica, no predicción
   - Transformación digital en gestión pública
   - Analogía con demand forecasting (hospitales, energía)

II. RELATED WORK (NUEVA)
   1. ML aplicado a seguridad ciudadana
   2. Pronóstico de denuncias e incidencia delictiva
   3. DSS para gestión pública
   4. Transformación digital e IA en sector público

III. METODOLOGÍA
   CRISP-DM (sin cambios)
   1. Tabla de Cronograma y Riesgos (Tabla 1)

IV. INGENIERÍA DE DATOS
   A. Auditoría de calidad del dataset
   B. Preparación y feature engineering

V. MODELADO
   A. Selección de algoritmos
   B. Variables del modelo
   C. Hiperparámetros

VI. RESULTADOS Y EVALUACIÓN
   A. Métricas de rendimiento (Tabla 2)
   B. Análisis de equidad
   C. Selección del modelo final

VII. DESPLIEGUE
   A. Arquitectura del sistema (Tabla 3)
   B. Plan de mantenimiento

VIII. DISCUSIÓN
   - Comparar con DSS y demand forecasting
   - Crítica honesta: denuncias ≠ criminalidad real
   - Referenciar Walczak, Hälterlein, Cesario

IX. CONCLUSIONES
   - Planificación institucional y asignación de recursos
   - No afirmar predicción de criminalidad real
   - Trabajo futuro: SMOGN/SMOTER, más variables

REFERENCIAS [1]-[15]
```

---

## 4. Referencias (15 total)

### Actuales que se mantienen (6)
| # | Referencia | Secciones |
|---|-----------|-----------|
| [1] | Sarker (2021) — ML survey | Intro, Metodología |
| [2] | Parsons & Torenvlied (2026) — Algoritmos + gobierno | Introducción |
| [3] | Shiraptini et al. (2026) — IA + ML en ciudades | Introducción |
| [4] | Guo (2026) — Fusión espacio-temporal | Introducción, Método |
| [5] | Hernández et al. (2026) — Fairness | Resultados, Discusión |
| [6] | Ministerio del Interior (2026) — Dataset SIDPOL | Metodología |

### Nuevas — del autor (6)
| # | Referencia | Categoría | Secciones |
|---|-----------|-----------|-----------|
| [7] | Walczak (2021) — Neural Networks in Police Decision Making | DSS | Related Work, Discusión |
| [8] | Hälterlein (2021) — Epistemologies of predictive policing | Crítica | Related Work, Discusión |
| [9] | Cesario et al. (2024) — Multi-density crime predictor | Forecasting | Related Work, Método |
| [10] | İlgün & Dener (2025) — Crime data + time series | Forecasting | Related Work, Método |
| [11] | Mandalapu et al. (2023) — Systematic review ML/DL crime | Survey | Related Work |
| [12] | Jenga et al. (2023) — ML in crime prediction survey | Survey | Related Work |

### Nuevas — complementarias de búsqueda (3)
| # | Referencia | Categoría | Secciones |
|---|-----------|-----------|-----------|
| [13] | Ashby (2023) — Forecasting crime trends → strategic decisions | DSS + Forecasting | Discusión |
| [14] | Branco et al. (2017) — SMOGN for imbalanced regression | Método | Metodología (nota futura) |
| [15] | Lin et al. (2025) — ED demand forecasting (analogía) | Demand Forecasting | Introducción, Discusión |

---

## 5. SMOTE — Corrección

### Estado actual del código
- `script_modelo_sidpol.py:741` → `"# sin SMOTE"` explícito
- Pipeline serializado: solo `preprocesador + modelo_rf`
- SMOTE importado pero NUNCA ejecutado

### Acciones
1. `app.py:132` — Cambiar log de `"Random Forest + SMOTE"` a `"Random Forest + OneHotEncoder"`
2. `app.py:211` — Eliminar mención a SMOTE del docstring
3. Artículo: **eliminar toda mención** a SMOTE en metodología y resultados
4. Opcional en Trabajo Futuro:
   > "En futuras versiones podrían evaluarse técnicas específicas para regresión, como SMOGN (Branco et al., 2017) o SMOTER, para abordar posibles desbalances en la variable objetivo."

---

## 6. Formato (nivel Avance 03)

| Aspecto | Valor |
|---------|-------|
| Papel | Carta Letter (8.5" × 11") |
| Márgenes | 0.5" uniformes |
| Interlineado | 1.5 (360 twips) |
| Columnas | 2, gap 360 |
| Fuente | Times New Roman (mantener) |
| Pie de página | Número de página centrado |
| Tablas | Estilo uniforme (List Table) |
| Keywords | Bullets (Prrafodelista) |
| Captions | Estilo Descripcin |
| Referencias | Numeradas [1]-[15] |
| Secciones | Numeración romana (I, II, III...) |

---

## 7. Imágenes

| # | Ubicación | Placeholder | Descripción |
|---|-----------|-------------|-------------|
| 1 | Introducción | [FIGURA 1: Vista del dataset SIDPOL] | Captura de Excel |
| 2 | Metodología | [FIGURA 2: Metodología CRISP-DM] | Diagrama (ya existe) |
| 3 | Ingeniería | [FIGURA 3: Código de preprocesamiento] | Captura de código |
| 4 | Ingeniería | [FIGURA 4: Head del dataset procesado] | Captura de datos |
| 5 | Modelado | [FIGURA 5: Código de entrenamiento RF] | Captura de código |
| 6 | Resultados | [FIGURA 6: Comparación de métricas] | Gráfico de barras |
| 7 | Despliegue | [FIGURA 7: Dashboard Angular] | Captura de pantalla |
| 8 | Despliegue | [FIGURA 8: Arquitectura microservicios] | Diagrama |

Se te darán instrucciones exactas para reemplazar cada placeholder.

---

## 8. Script Python

Archivo: `motor_Sidpol/mejorar_articulo.py`

```
hacer_copia()                          → Backup
ajustar_formato_general()              → Letter, márgenes, interlineado, footer
agregar_tabla_article_info()           → Tabla ARTICLE INFO al inicio
convertir_keywords_a_lista()           → Bullets para keywords
convertir_captions_a_estilo()          → Estilo Descripcin
agregar_placeholders_imagenes()        → [FIGURA X: ...]
cambiar_titulo()                       → Nuevo título
nombre_secciones_a_romanas()           → I, II, III...
convertir_referencias_a_numeradas()    → [1]-[15]
reemplazar_vocabulario()              → Viejo → nuevo narrativo
mejorar_tablas_existentes()            → Formato a 3 tablas
main()                                 → Orquestador
```

---

## 9. Pendiente del autor para completar

- [ ] Imágenes reales para reemplazar los 8 placeholders
- [ ] Revisión final de referencias con DOIs correctos
- [ ] Confirmar si deseas que genere los gráficos (Figura 6) desde `metricas_sidpol.json` automáticamente

---

## Resumen de cambios

| Dimensión | Cambio |
|-----------|--------|
| **Narrativa** | "Predicción de crimen" → "Pronóstico de denuncias (DSS)" |
| **Título** | Nuevo (enfocado en pronóstico + planificación estratégica) |
| **Related Work** | **Nueva sección** (4 bloques) |
| **Referencias** | 6 → **15** (con DOIs) |
| **SMOTE** | Eliminado de toda la documentación |
| **Formato** | A4 variable → **Letter + 0.5" + 1.5 interlineado** |
| **Secciones** | Numeración arábiga → **Romana** |
| **Keywords** | Texto plano → **Bullets** |
| **Captions** | Texto plano → **Estilo Descripcin** |
| **Pie de página** | No tenía → **Número de página** |
| **Tabla ARTICLE INFO** | No tenía → **Agregada al inicio** |
| **Modelo/Métricas/Arquitectura** | **Sin cambios** |
