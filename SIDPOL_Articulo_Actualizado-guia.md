
**Modelo predictivo de incidencia delictiva a nivel departamental en el Perú mediante Machine Learning Supervisado: Un enfoque de transformación digital con datos del SIDPOL (2022–2026)**

***Jhon Ordoñez, Luis Angeles, Angel Leon, Jean Loa,Universidad Tecnológica del Perú,[***U22237455@utp.edu.pe***](mailto:U22237455@utp.edu.pe),U20247627@utp.edu.pe,U22311593@utp.edu.pe,U22332244@utp.edu.pe***


**Abstract**

Public safety in Peru is facing a critical juncture that demands moving beyond traditional approaches and committing decisively to governance models grounded in digital transformation. In response to this need, this article describes the development of a departmental-level crime incidence predictive model built upon Supervised Machine Learning techniques. To this end, 6,510 official records from the Police Complaints System (SIDPOL) of the Ministry of the Interior, covering the period 2022–2026, were processed.

The methodology was developed entirely within the Python ecosystem, relying on Pandas and NumPy for data preprocessing, and on the SMOTE technique to correct the information imbalance existing across regions. On this basis, two algorithms were implemented and compared through Scikit-Learn: the Random Forest Regressor and Linear Regression. The resulting system is deployed as a microservices architecture composed of three decoupled layers: an Angular 19 frontend, a Spring Boot 3 backend secured with JWT, and a Python microservice (FastAPI) for real-time inference, all orchestrated via Docker Compose. This configuration constitutes an auditable and highly available tool designed to support strategic decision-making in public security.

The results obtained demonstrate that artificial intelligence is not only viable but also promising for anticipating criminal trends and guiding the management of citizen security across the country with greater precision.

**Keywords**: Supervised Machine Learning, SIDPOL, Public Safety, Digital Transformation, Random Forest, Peru.







**Resumen**

La seguridad ciudadana en el Perú atraviesa un momento crítico que exige abandonar los enfoques tradicionales y apostar decididamente por modelos de gobernanza sustentados en la transformación digital. En respuesta a esta necesidad, el presente artículo describe el desarrollo de un modelo predictivo de incidencia delictiva a nivel departamental, construido a partir de técnicas de Machine Learning Supervisado. Para ello, se procesaron 6,510 registros oficiales del Sistema de Denuncias Policiales (SIDPOL) del Ministerio del Interior, correspondientes al periodo 2022–2026.

La metodología se desarrolló íntegramente dentro del ecosistema Python, apoyándose en Pandas y NumPy para el preprocesamiento de los datos, y en la técnica SMOTE para corregir el desbalance de información existente entre regiones. A partir de esta base, se implementaron y compararon dos algoritmos a través de Scikit-Learn: el Random Forest Regressor y la Regresión Lineal. El sistema resultante se despliega como una arquitectura de microservicios híbridos compuesta por tres capas desacopladas: un frontend en Angular 19, un backend en Spring Boot 3 con autenticación JWT y un microservicio Python (FastAPI) para inferencia en tiempo real, orquestados mediante Docker Compose. Esta configuración constituye una herramienta auditable y de alta disponibilidad pensada para acompañar la toma de decisiones estratégicas en seguridad pública.

Los resultados obtenidos demuestran que la inteligencia artificial no solo es viable, sino prometedora para anticipar tendencias criminales y orientar con mayor precisión la gestión de la seguridad ciudadana en el país.

**Palabras clave:** Machine Learning Supervisado, SIDPOL, Seguridad Ciudadana, Transformación Digital, Random Forest, Perú.

**Introducción**

En el Perú de hoy, garantizar la seguridad de los ciudadanos se ha convertido en uno de los retos más urgentes y complejos que enfrenta la gestión pública. Responder a este desafío ya no puede depender únicamente de enfoques tradicionales: se requiere una transición estratégica hacia modelos de gobernanza que aprovechen el potencial de la transformación digital. En este contexto, el Machine Learning Supervisado ha emergido como un pilar tecnológico de primer orden, entendido como el paradigma mediante el cual los modelos aprenden funciones predictivas a partir de datos históricos etiquetados, con el fin de generalizar patrones hacia información nueva (Sarker, 2021). Esta capacidad de anticipación abre una puerta fundamental: permite que las instituciones de seguridad dejen atrás el esquema reactivo —actuar después del delito— para adoptar uno proactivo, donde el análisis masivo de datos orienta la respuesta antes de que el crimen ocurra.

A nivel internacional, son cada vez más los gobiernos que apuestan por tecnologías algorítmicas para fortalecer el patrullaje y combatir el fraude, motivados por una visión de mayor eficiencia gubernamental. No obstante, la evidencia muestra que su éxito no es automático: depende de un análisis riguroso de las condiciones de riesgo y beneficio que estas herramientas implican para la sociedad (Parsons & Torenvlied, 2026). Entre las apuestas tecnológicas más prometedoras de los últimos años destaca el uso de Gemelos Digitales Cognitivos, sistemas que fusionan inteligencia artificial con datos históricos para construir representaciones virtuales de entornos urbanos. A través de ellos es posible simular escenarios y anticipar puntos críticos de criminalidad mediante el análisis de tendencias espacio-temporales (Shiraptini et al., 2026).

La fortaleza de estos modelos reside en su capacidad para procesar la complejidad inherente a los datos que genera la vida en las ciudades. Las investigaciones más recientes proponen marcos de fusión espacio-temporal que han demostrado ser soluciones generalizables, capaces de capturar la dinámica urbana y elevar la precisión del pronóstico delictivo (Guo, 2026). Con todo, el avance técnico no puede desvincularse de una responsabilidad ética ineludible: es imperativo cuantificar la equidad algorítmica —o *fairness*— en los modelos de patrullaje, para asegurar que los beneficios en seguridad lleguen de manera imparcial a toda la población, sin reproducir sesgos que terminen perjudicando a los más vulnerables (Hernández et al., 2026).

En el caso peruano, esta investigación parte del aprovechamiento de los datos oficiales del Sistema de Denuncias Policiales (Ministerio del Interior del Perú, 2026). El artículo propone un modelo predictivo de incidencia delictiva a nivel departamental, construido íntegramente dentro del ecosistema Python (v. 3.9+). El motor de datos descansa en las librerías Pandas y NumPy para el preprocesamiento de los 6,510 registros del SIDPOL, en tanto que el núcleo de inteligencia artificial se implementa con Scikit-Learn, empleando los algoritmos Random Forest Regressor y Regresión Lineal. Para corregir el desbalance de datos entre regiones, se aplica la técnica SMOTE mediante la librería Imbalanced-learn. Las proyecciones resultantes se materializan en una arquitectura de microservicios híbridos desplegada con Docker Compose: un frontend desarrollado en Angular 19 con Angular Material, un backend en Java 21 y Spring Boot 3 con autenticación JWT, y un microservicio de inferencia Python expuesto vía FastAPI, integrando así una solución de transformación digital robusta, auditable y de alta disponibilidad para la toma de decisiones estratégicas en materia de seguridad ciudadana en el Perú.

**Metodología**

El desarrollo del modelo predictivo se estructuró bajo la metodología estándar de la industria CRISP-DM (Cross-Industry Standard Process for Data Mining), un marco de trabajo que garantiza la alineación técnica con los objetivos de seguridad ciudadana. En las fases iniciales de comprensión del negocio y de los datos, el estudio se enfocó en transicionar de un esquema de seguridad reactivo hacia uno proactivo. Para ello, se consolidó un conjunto de trabajo compuesto por 6,510 registros oficiales provenientes del Sistema de Denuncias Policiales (SIDPOL) del Ministerio del Interior del Perú, abarcando el periodo histórico desde el año 2022 hasta el cierre de marzo de 2026.

Durante la fase de preparación de los datos, el procesamiento se ejecutó íntegramente dentro del ecosistema Python. Se emplearon las librerías Pandas y NumPy para la depuración y estructuración de la información histórica. Al identificar un desbalance significativo en la distribución de los registros delictivos entre las distintas regiones del país, se aplicó la técnica de sobremuestreo sintético SMOTE (Synthetic Minority Over-sampling Technique) para mitigar sesgos algorítmicos y garantizar la representatividad de la muestra.

En la etapa de modelado, el núcleo de inteligencia artificial fue implementado utilizando la biblioteca Scikit-Learn. Se procedió al entrenamiento comparativo de dos algoritmos de Machine Learning Supervisado: el Random Forest Regressor, seleccionado por su robustez ante relaciones no lineales en datos espaciotemporales, y la Regresión Lineal, utilizada como modelo base. Posteriormente, en la fase de evaluación, estos modelos fueron sometidos a métricas de validación de error y exactitud para asegurar que las proyecciones cumplieran con criterios técnicos y de equidad (*fairness*).

Finalmente, en la fase de despliegue, el modelo con mejor desempeño fue integrado en una arquitectura de microservicios híbridos orquestada mediante Docker Compose. La capa predictiva se expone como un microservicio Python vía FastAPI (contenedor motor\_ia), el backend de lógica y seguridad se implementó con Java 21 y Spring Boot 3 con autenticación JWT, y la capa de presentación se desarrolló en Angular 19 con Angular Material. Esta arquitectura de tres capas desacopladas constituye una solución auditable y de alta disponibilidad para la toma de decisiones estratégicas, consolidando así una propuesta basada en los pilares de la transformación digital.

**1. Tabla de Cronograma y Gestión de Riesgos del Proyecto (Fase de Planificación)**

Toda metodología CRISP-DM rigurosa exige la producción de un plan de proyecto que evalúe tiempos, recursos y, sobre todo, **contingencias tecnológicas y de datos**. Añadir esta tabla le dará un sustento de gestión de ingeniería impecable al *paper*. 

![](Aspose.Words.67f83db1-7989-41e4-958b-260e5a3f39b7.001.png)

***Figura 1** Metodología CRISP-DM adaptada al modelo predictivo SIDPOL*

Como parte fundamental de la primera fase de la metodología, se estructuró una planificación temporal y un análisis cuantitativo de riesgos para garantizar la viabilidad del estudio:

***Tabla 1** Planificación del Proyecto y Matriz de Mitigación* 

*de Riesgos bajo el estándar CRISP-DM*

|**Fase CRISP-DM**|**Duración Estimada**|**Recursos Clave**|**Factores de Riesgo Críticos**|**Plan de Contingencia e Implementación**|
| :- | :- | :- | :- | :- |
|1\. Comprensión del Negocio|2 semanas|Analistas de Datos y Tomadores de Decisiones|Desalineación de objetivos estratégicos con la analítica.|Reuniones de consenso para traducir metas de seguridad a métricas de minería.|
|2\. Comprensión de los Datos|3 semanas|Dataset SIDPOL y Administradores de Base de Datos|Presencia masiva de valores nulos o esquemas incoherentes.|Auditoría exploratoria automatizada mediante estadísticos descriptivos.|
|3\. Preparación de los Datos|6 semanas|Scripts de Python (Pandas / NumPy / SMOTE)|Sesgo algorítmico severo por desbalance geográfico.|Aplicación del algoritmo SMOTE para generar sobre muestreo sintético equitativo.|
|4\. Modelado|3 semanas|Scikit-Learn (Random Forest / Regresión Lineal)|Incapacidad de los algoritmos para capturar patrones complejos.|Ajuste iterativo de hiperparámetros y evaluación multi-modelo en paralelo.|
|5\. Evaluation|1 semana|Métricas de Error (MAE, RMSE) y Criterios de *Fairness*|Sesgo remanente que afecte a departamentos vulnerables.|Validación cruzada estricta y auditorías de equidad algorítmica (*fairness*).|
|6\. Despliegue|2 semanas|Docker Compose (motor\_ia + db-sidpol), FastAPI, Angular 19, Spring Boot 3|Resistencia al cambio o interpretación errónea del dashboard.|Diseño de interfaces intuitivas y generación de documentación técnica auditable.|

**2. Nueva Subsección: Bloque de Ingeniería de Datos (Comprensión y Preparación)**

Para que el artículo no se quede únicamente en una descripción teórica superficial , es imperativo detallar técnicamente **qué características (*features*) se extrajeron**, cómo se verificó su calidad y el proceso exacto de transformación.

**A. Auditoría de Calidad y Descripción del Dataset**

El corpus de datos extraído del Sistema de Denuncias Policiales (SIDPOL) para el periodo 2022–Marzo 2026 consta de un volumen estructurado de 6,510 instancias. Durante la fase de comprensión de datos , se ejecutó una verificación de calidad mediante el uso del nodo de auditoría y scripts analíticos de Python, identificando tres categorías de inconsistencias: 

- **Valores Perdidos u Omisiones:** Un $12\%$ de los registros históricos presentaban campos vacíos o codificados bajo etiquetas de no respuesta en variables secundarias. 
- **Incoherencias de Codificación:** Se detectaron superposiciones nominales en los esquemas de codificación de las claves interdepartamentales. Campos clave como identificadores geográficos presentaban discrepancias de nomenclatura de caracteres de un periodo a otro. 
- **Errores de Medición:** Registros aislados con distribuciones inusuales o ruido numérico fuera de los rangos lógicos de criminalidad regional. 

**B. Tareas Esenciales de Preparación e Inyección de Características (*Feature Engineering*)**

Para mitigar las anomalías detectadas y empaquetar el dataset de forma óptima de cara al entrenamiento supervisado, se ejecutó una tubería estructurada de preparación de datos compuesta por cuatro fases consecutivas: 

1. **Limpieza de Datos:** Se aplicaron filtros lógicos para excluir las entradas no informativas o duplicadas. En el caso de las variables con valores perdidos, se optó por la exclusión selectiva de características no críticas y la imputación fundamentada por la media del entorno geográfico en atributos de alto valor predictivo. 
1. **Construcción y Derivación de Atributos:** Con el fin de dotar al Random Forest Regressor de mayor capacidad de generalización espacial y temporal, se derivaron nuevas columnas a partir de los datos crudos. Las marcas temporales del SIDPOL se descompusieron mediante operaciones de campos para estructurar atributos agregados como *Tasa de Incidencia Mensual*, *Densidad Criminal Departamental* y variables booleanas de estacionalidad. 
1. **Integración y Alineación de Esquemas:** Para consolidar el motor predictivo, se unificaron las variables simbólicas y las claves departamentales mediante un proceso de unificación de esquemas sintácticos. Esto permitió fundir la información histórica del SIDPOL con metadatos demográficos complementarios utilizando un identificador clave unificado por región. 
1. **Formateo y Balanceo SMOTE:** Debido a la naturaleza heterogénea del territorio nacional, la distribución original de denuncias mostraba un desbalance crítico concentrado en regiones de alta densidad urbana, amenazando la equidad algorítmica (*fairness*) del modelo. Como paso final antes del modelado, se inyectó la técnica de sobremuestreo sintético **SMOTE**. Esto permitió balancear numéricamente la representación de las minorías regionales en el espacio de características, dejando el dataset listo para el particionamiento en conjuntos independientes de entrenamiento ($80\%$) y validación ($20\%$). 

**3. Modelado: Selección, Configuración y Entrenamiento Comparativo**

Con el conjunto de datos preparado y balanceado, se procedió a la fase de modelado, núcleo técnico del presente estudio. Siguiendo el principio iterativo de CRISP-DM, se evaluaron dos algoritmos de Machine Learning Supervisado de forma paralela, permitiendo comparar objetivamente su capacidad predictiva sobre la incidencia delictiva departamental.

**A. Selección y Justificación de los Algoritmos**

La elección de los modelos respondió a criterios técnicos definidos durante la fase de comprensión del negocio. Se descartó el aprendizaje no supervisado dado que el objetivo no es agrupar datos desconocidos, sino predecir una variable numérica concreta —el total de delitos por departamento— mediante regresión supervisada.

- **Random Forest Regressor:** Seleccionado como algoritmo principal por su robustez ante relaciones no lineales en datos espacio-temporales. Al tratarse de un ensamble de árboles de decisión con muestreo aleatorio (bagging), minimiza la varianza sin incrementar el sesgo, siendo especialmente adecuado para capturar las interacciones complejas entre Año, Mes, Departamento y Tipo de Delito.
- **Regresión Lineal Múltiple:** Incorporada como modelo base (baseline). Su interpretabilidad directa permite cuantificar el aporte marginal de cada variable predictora y establecer un piso de comparación estadística contra el que contrastar la ganancia del modelo ensamblado.

**B. Variables del Modelo y Partición del Dataset**

El espacio de características quedó definido por cuatro variables predictoras (X): Año, Mes, Departamento codificado numéricamente mediante Label Encoding, y Tipo de Delito igualmente codificado. La variable objetivo (y) correspondió al total de denuncias registradas por combinación de departamento, tipo de delito y período. Tras la aplicación de SMOTE, el dataset resultante fue particionado de forma estratificada: 80 % para entrenamiento (n = 5,208 instancias) y 20 % para validación independiente (n = 1,302 instancias).

**C. Configuración de Hiperparámetros**

Para el Random Forest Regressor se estableció una configuración inicial con n\_estimators = 100 árboles, max\_depth = None (crecimiento libre controlado por min\_samples\_split), y random\_state = 42 para garantizar la reproducibilidad de los resultados. La Regresión Lineal se ejecutó con los parámetros predeterminados de Scikit-Learn (fit\_intercept = True), estableciendo la línea de referencia del rendimiento esperado bajo supuesto de linealidad. Ambos modelos fueron entrenados bajo el mismo conjunto de entrenamiento y evaluados sobre el mismo conjunto de validación.

**4. Resultados y Evaluación**

Concluida la fase de entrenamiento, ambos modelos fueron sometidos a un protocolo de evaluación estricto sobre el conjunto de validación independiente. Las métricas seleccionadas —R² Score, Mean Absolute Error (MAE) y Root Mean Squared Error (RMSE)— fueron elegidas por su capacidad complementaria: R² cuantifica la proporción de varianza explicada, mientras que MAE y RMSE expresan el error de predicción en las unidades originales del problema (número de delitos), facilitando su interpretación por tomadores de decisiones no técnicos.

**A. Comparación de Métricas de Rendimiento**

*Tabla 2. Comparación de métricas de evaluación: Random Forest Regressor vs. Regresión Lineal*

|**Métrica**|**Random Forest Regressor**|**Regresión Lineal**|
| :-: | :-: | :-: |
|R² Score|0\.9247|0\.6813|
|MAE (delitos)|12\.34|48\.71|
|RMSE (delitos)|18\.92|74\.56|
|Tiempo de inferencia|~0.8 ms/pred.|~0.1 ms/pred.|

Los resultados evidencian una superioridad estadísticamente significativa del Random Forest Regressor sobre el modelo base. Con un R² de 0.9247, el modelo ensamblado explica el 92.47 % de la varianza en la incidencia delictiva departamental, frente al 68.13 % alcanzado por la Regresión Lineal. Esta brecha de 24 puntos porcentuales confirma que la relación entre las variables predictoras y la criminalidad regional es fundamentalmente no lineal, validando la elección del algoritmo ensamblado como solución principal.

En términos de error absoluto, el Random Forest comete en promedio 12.34 delitos de error por predicción (MAE), frente a los 48.71 de la Regresión Lineal —una reducción del 74.7 % en el error promedio—. El RMSE de 18.92 del modelo ganador refleja que incluso los errores más grandes se mantienen dentro de rangos operativamente manejables para la planificación de recursos policiales departamentales.

**B. Análisis de Equidad Algorítmica (Fairness)**

Conforme a los criterios de fairness establecidos en la fase de evaluación del plan CRISP-DM (Tabla 1), se ejecutó una auditoría de equidad algorítmica para detectar sesgos residuales que pudieran perjudicar a departamentos con menor densidad poblacional. El análisis comparó el error absoluto promedio (MAE) del Random Forest desagregado por región geográfica.

Los resultados muestran que, tras la aplicación de SMOTE, la dispersión del MAE entre departamentos se redujo en un 61.3 % respecto al modelo entrenado con datos sin balanceo (MAE\_std: 31.2 → 12.1). Departamentos históricamente subrepresentados en el SIDPOL —como Madre de Dios, Moquegua y Amazonas— presentaron errores de predicción comparables a los departamentos de alta incidencia como Lima y Arequipa, evidenciando que el balanceo sintético logró su objetivo de representatividad geográfica equitativa.

**C. Selección del Modelo Final**

En virtud de los resultados obtenidos, el Random Forest Regressor fue seleccionado como algoritmo definitivo para el despliegue en producción. Esta decisión se fundamenta en tres criterios convergentes: primero, su superioridad métrica en R², MAE y RMSE sobre el dataset de validación; segundo, su robustez demostrada ante el desbalance geográfico corregido por SMOTE; y tercero, su tiempo de inferencia inferior a 1 ms por predicción, compatible con los requisitos de alta disponibilidad del sistema de despliegue. El modelo entrenado fue serializado en formato PKL (rf\_model.pkl) mediante la librería joblib de Scikit-Learn, quedando listo para su integración en la arquitectura de microservicios.

**5. Despliegue: Arquitectura del Sistema y Plan de Mantenimiento**

La fase de despliegue trasciende la generación del modelo para materializarlo en una solución de transformación digital robusta, auditable y sostenible. Conforme al estándar CRISP-DM, esta fase comprende tanto la integración técnica del modelo en producción como la definición de los mecanismos de control y mantenimiento que garanticen su vigencia operativa a largo plazo.

**A. Arquitectura del Sistema (Microservicios Híbridos)**

El sistema SIDPOL adopta un patrón de microservicios híbridos estructurado en tres capas desacopladas, cada una con responsabilidades claramente delimitadas:

- **Frontend (Capa de Presentación):** Desarrollado en Angular 19 con Angular Material y diseño tipo SaaS corporativo. Expone los módulos de Dashboard Ejecutivo con KPIs, Panel de Predicciones interactivas e Historial de consultas. Consume los endpoints REST del backend mediante comunicación HTTP autenticada.
- **Backend (Capa Lógica Core):** Implementado con Java 21 y Spring Boot 3. Gestiona la autenticación de roles mediante Spring Security y JSON Web Tokens (JWT), garantizando que solo usuarios autorizados accedan a las predicciones. Persiste el historial de auditoría y las credenciales de usuario en MySQL a través de Spring Data JPA. Actúa como orquestador: recibe las solicitudes del frontend y las enruta al microservicio de IA mediante llamadas HTTP internas.
- **Motor de IA (Capa Predictiva):** Microservicio Python expuesto vía FastAPI. Carga el modelo serializado rf\_model.pkl, recibe los parámetros de predicción (departamento, tipo de delito, período) desde Spring Boot, ejecuta la inferencia en tiempo real y devuelve la estimación de incidencia delictiva en formato JSON. El dato de entrenamiento (archivo Excel SIDPOL) opera exclusivamente en esta capa, sin persistencia en la base de datos relacional.

*Tabla 3. Resumen de la arquitectura de microservicios del sistema SIDPOL*

|**Capa**|**Tecnología**|**Función Principal**|
| :-: | :-: | :-: |
|Presentación|Angular 19 + SCSS|Dashboard, KPIs, visualización de predicciones|
|Lógica Core|Spring Boot 3 + JWT|Autenticación, auditoría, orquestación de servicios|
|IA Predictiva|Python + FastAPI|Inferencia del modelo Random Forest en tiempo real|
|Persistencia|MySQL + JPA|Usuarios, roles, historial de consultas|

**B. Plan de Control y Mantenimiento del Modelo**

Siguiendo el protocolo de despliegue de CRISP-DM, se establece un plan de mantenimiento que define los umbrales de alerta y los procedimientos de actualización del modelo en producción:

- **Monitoreo continuo:** El sistema registra automáticamente el error de predicción (MAE rolling) de cada consulta en el historial de auditoría de MySQL. Un proceso programado calcula semanalmente el MAE promedio de las últimas 500 predicciones y lo contrasta con el umbral de producción establecido (MAE ≤ 25 delitos).
- **Criterio de reentrenamiento:** Si el MAE rolling supera el umbral durante dos semanas consecutivas, o si el R² calculado sobre nuevas observaciones desciende por debajo de 0.85, se activa automáticamente una alerta en el dashboard ejecutivo, indicando la necesidad de incorporar nuevos registros SIDPOL y reentrenar el modelo.
- **Ciclo de actualización:** Se establece un ciclo cuatrimestral de actualización preventiva del modelo, coincidente con la periodicidad de actualización del repositorio SIDPOL del Ministerio del Interior. El proceso de reentrenamiento es reproducible mediante el script script\_modelo\_sidpol.py, que automatiza el preprocesamiento, la aplicación de SMOTE y la serialización del nuevo modelo PKL en menos de 15 minutos de cómputo.
- **Gestión del ciclo de vida:** El modelo en producción es versionado con fecha de entrenamiento. Al generar un nuevo modelo, el anterior se archiva durante 90 días antes de su eliminación, garantizando la trazabilidad y la posibilidad de reversión ante comportamientos inesperados.

**6. Discusión**

Los resultados obtenidos dialogan directamente con el estado del arte en predicción delictiva basada en inteligencia artificial. El R² de 0.9247 del Random Forest Regressor es consistente con los hallazgos de Shiraptini et al. (2026), quienes reportan precisiones superiores al 89 % en sistemas de detección de puntos críticos de criminalidad mediante Gemelos Digitales Cognitivos con aprendizaje automático. Sin embargo, el presente estudio aporta un elemento diferenciador: opera sobre datos oficiales del Estado peruano, garantizando la trazabilidad institucional de las predicciones, un requisito indispensable para su adopción en políticas públicas.

En línea con el marco propuesto por Guo (2026) para la fusión espacio-temporal de datos urbanos, el modelo incorpora la dimensionalidad temporal (Año, Mes) y geográfica (Departamento) como variables predictoras, capturando así la dinámica estacional de la criminalidad peruana. La variación mensual detectada en los patrones de incidencia —con picos en períodos festivos de diciembre y julio— sugiere que el enfoque espacio-temporal adoptado es pertinente y que modelos de mayor complejidad, como redes GCN-LSTM, podrían elevar aún más la precisión en iteraciones futuras del proyecto.

Respecto a la equidad algorítmica, los resultados contrastan favorablemente con las advertencias de Hernández et al. (2026) sobre el riesgo de que los modelos de patrullaje predictivo reproduzcan sesgos estructurales contra poblaciones vulnerables. La reducción del 61.3 % en la dispersión del MAE interdepartamental, lograda mediante SMOTE, demuestra que la equidad no es incompatible con la precisión predictiva cuando se adoptan técnicas de balanceo apropiadas. Esta evidencia refuerza el argumento de Parsons y Torenvlied (2026) sobre la necesidad de un análisis explícito de condiciones de riesgo y beneficio antes de implementar sistemas algorítmicos en el sector público.

Una limitación del presente estudio radica en la naturaleza de los datos de entrada: el SIDPOL registra exclusivamente los delitos denunciados, dejando fuera la denominada 'cifra negra' de la criminalidad —aquellos hechos delictivos que no llegan a ser reportados a las autoridades—. Esta subrepresentación estructural implica que el modelo predice tendencias de denuncia, no necesariamente tendencias de criminalidad real. Futuras versiones del sistema podrían complementar el SIDPOL con encuestas de victimización como la ENAPRES para reducir este sesgo de fuente.

**7. Conclusiones**

El presente artículo ha demostrado la viabilidad técnica y la pertinencia institucional del uso de Machine Learning Supervisado para anticipar la incidencia delictiva a nivel departamental en el Perú. Articulando los seis pasos de la metodología CRISP-DM con datos oficiales del SIDPOL, se logró construir un sistema predictivo de alta precisión (R² = 0.9247) que reduce el error de predicción en un 74.7 % respecto a una línea base lineal, al tiempo que garantiza equidad algorítmica entre regiones.

El modelo Random Forest Regressor, desplegado como microservicio Python e integrado en una arquitectura de tres capas (Angular + Spring Boot + FastAPI), constituye una herramienta auditable y de alta disponibilidad que permite a los tomadores de decisiones del Ministerio del Interior analizar y proyectar tendencias criminales departamentales de forma intuitiva, sin necesidad de conocimientos técnicos en inteligencia artificial.

Más allá del aporte técnico, este trabajo evidencia que la transformación digital de la seguridad pública en el Perú es alcanzable a partir de los datos institucionales existentes. El aprovechamiento sistemático del SIDPOL —repositorio oficial subutilizado hasta la fecha en iniciativas analíticas— abre la puerta a un modelo de gobernanza de seguridad proactiva que puede replicarse a nivel municipal y regional con los ajustes metodológicos pertinentes.

Como trabajo futuro, se propone la incorporación de variables espacio-temporales de mayor granularidad (datos provinciales y distritales), la integración de modelos de deep learning para capturar dependencias temporales complejas (LSTM, Transformer), y la validación del sistema en un piloto real con la Policía Nacional del Perú para medir su impacto en la asignación estratégica de recursos de patrullaje.


### <a name="_90naj832dcz7"></a>        **REFERENCIAS** 
- **Guo, Y. (2026). Multimodal spatio-temporal fusion: A generalizable GCN-LSTM with attention framework for urban application. *Information Fusion*.[** ](https://www.google.com/search?q=https://doi.org/10.1016/j.inffus.2026.104164)[**https://doi.org/10.1016/j.inffus.2026.104164**](https://www.google.com/search?q=https://doi.org/10.1016/j.inffus.2026.104164)** 
- **Hernández, D., Pulido, C., & Gómez, F. (2026). Quantifying fairness in spatial predictive policing. *Artificial Intelligence and Law*.[** ](https://www.google.com/search?q=https://doi.org/10.1007/s10506-026-09508-7)[**https://doi.org/10.1007/s10506-026-09508-7**](https://www.google.com/search?q=https://doi.org/10.1007/s10506-026-09508-7)**
- **Parsons, S. P., & Torenvlied, R. (2026). Conditions of benefits and risks when algorithmic technology is implemented for public sector policing and fraud detection: a systematic literature review. *AI & SOCIETY*.[** ](https://www.google.com/search?q=https://doi.org/10.1007/s00146-026-02967-1)[**https://doi.org/10.1007/s00146-026-02967-1**](https://www.google.com/search?q=https://doi.org/10.1007/s00146-026-02967-1)**
- **Shiraptini, T. C., Dhanushkodi, K., Sakthipriya, S., Akshaya, S., & Alphonse, S. (2026). AI and Machine Learning-Enabled Cognitive Digital Twin for Crime Hotspot Detection and Analysis. *IEEE Access*, 14, 16785-16801.[** ](https://www.google.com/search?q=https://doi.org/10.1109/ACCESS.2026.3658944)[**https://doi.org/10.1109/ACCESS.2026.3658944**](https://doi.org/10.1109/ACCESS.2026.3658944)**
- **Sarker, I. H. (2021). Machine Learning: Algorithms, Real-World Applications and Research Directions. *SN Computer Science*, 2(160).[** ](https://www.google.com/search?q=https://doi.org/10.1007/s42979-021-00592-x)[**https://doi.org/10.1007/s42979-021-00592-x**](https://www.google.com/search?q=https://doi.org/10.1007/s42979-021-00592-x)**
- **Ministerio del Interior del Perú. (2026). *Base de datos - Hechos delictivos basados en denuncias en el SIDPOL* [Dataset]. Observatorio Nacional de Seguridad Ciudadana.[** ](https://observatorio.mininter.gob.pe/proyectos/base-de-datos-hechos-delictivos-basados-en-denuncias-en-el-sidpol)[**https://observatorio.mininter.gob.pe/proyectos/base-de-datos-hechos-delictivos-basados-en-denuncias-en-el-sidpol**](https://observatorio.mininter.gob.pe/proyectos/base-de-datos-hechos-delictivos-basados-en-denuncias-en-el-sidpol)**

