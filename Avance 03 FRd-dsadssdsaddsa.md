![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.001.png)

**PREDICCIÓN DEL RIESGO CREDITICIO CON MACHINE LEARNING**

***CREDIT RISK PREDICTION WITH MACHINE LEARNING***

Huaripata García, Carlos Daniel¹; Arzapalo Mantilla, Neison Ering¹, Peralta Rafael, Katherine Fabiana¹, Jian Pier Santiago Hurtado Alvarez¹, Milagros Nicole, Armas Pelayo¹.

*¹ Universidad Tecnológica del Perú, Lima, Perú.*

[*U18311691@utp.edu.pe*](mailto:U18311691@utp.edu.pe)*, [*U22238134@utp.edu.pe*](mailto:U22238134@utp.edu.pe) , [*U22206763@utp.edu.pe*](mailto:U22206763@utp.edu.pe), [*U23208436@utp.edu.pe*](mailto:U23208436@utp.edu.pe), [*U22212507@utp.edu.pe*](mailto:U22212507@utp.edu.pe).*

*Docente: Nilton Omar Santillán Aching | Área: Innovación y Transformación Digital*

|**ARTICLE INFO**|**RESUMEN**|
| :- | :- |
|<p>**Palabras clave:** </p><p>Riesgo crediticio</p><p>Machine learning</p><p>Árbol de decision</p><p>Credit scoring</p><p>Scikit-learn A</p>|La evaluación del riesgo crediticio es una tarea crítica en el sector financiero. En este trabajo se desarrolla un modelo de predicción basado en un Árbol de Decisión (DecisionTreeClassifier), entrenado sobre un dataset bancario real de 26000 registros con variables socioeconómicas de clientes (edad, provincia, estado civil, número de hijos, tipo de trabajo, sueldo, deuda e historial de pago). El modelo fue implementado en Python utilizando las librerías pandas y scikit-learn en Google Colab. La exactitud obtenida fue de 92% sobre el conjunto de prueba (20%). Se discute el impacto del desbalance de datos y se proponen mejoras para futuros trabajos.|

5

ABSTRACT

Credit risk assessment is a critical task in the financial sector. This paper develops a prediction model based on a Decision Tree classifier trained on a real banking dataset of 26000 records including socioeconomic client variables (age, province, marital status, number of children, employment type, salary, debt, and payment history). The model was implemented in Python using pandas and scikit-learn libraries in Google Colab. The accuracy obtained was 92% on the test set (20%). The impact of class imbalance is discussed and improvements are proposed for future work.

**I. INTRODUCCIÓN**

En el sector financiero, la evaluación del riesgo crediticio es un proceso fundamental para la toma de decisiones vinculadas a la aprobación de préstamos y la gestión de carteras de clientes. Tradicionalmente, este análisis se realiza mediante métodos estadísticos clásicos y reglas predefinidas, limitando la detección de patrones complejos en los datos de los solicitantes [1].

El uso de técnicas de Machine Learning (ML) representa una alternativa de alto potencial, permitiendo analizar grandes volúmenes de información con múltiples variables socioeconómicas simultáneamente. Estudios recientes han demostrado que la aplicación de ML mejora significativamente los sistemas de credit scoring, distinguiendo de manera más eficiente entre clientes con buen y mal comportamiento crediticio [2].

El desarrollo de modelos basados en gradient boosting ha permitido además incorporar datos no tradicionales y mejorar la capacidad predictiva en economías emergentes de América Latina [3]. Sin embargo, el uso extendido de estos modelos genera desafíos vinculados a la interpretabilidad, equidad y transparencia en sistemas automatizados de decisión [4]. La literatura también señala problemas como el desbalance de clases en los conjuntos de datos, que puede afectar el rendimiento del modelo [5].

En este contexto, el presente trabajo tiene como objetivo desarrollar un modelo de ML para la predicción del riesgo crediticio utilizando un Árbol de Decisión entrenado sobre un dataset bancario peruano real. La pregunta de investigación es: ¿En qué medida un modelo de Árbol de Decisión puede predecir el nivel de riesgo crediticio de un cliente a partir de sus variables socioeconómicas?

**II. DESCRIPCIÓN DEL CONJUNTO DE DATOS**

El dataset utilizado ("data Banco F.xlsx") contiene información socioeconómica real de clientes de una institución financiera peruana. A continuación, se muestran las primeras filas tal como fueron cargadas en Google Colab:

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.002.png)

*Ilustración *1*. Vista del dataset "data Banco F.xlsx" en Microsoft Excel*




El dataset contiene 26000 registros y las siguientes variables:

***Tabla ***1***. Variables del dataset bancario***

|**Variable**|**Descripción**|**Tipo**|**Rol**||
| :-: | :-: | :-: | :-: | :- |
|DNI|Identificador del cliente|Numérica|ID||
|Edad|Años del cliente|Numérica|Entrada||
|Provincia|Ciudad de residencia|Categórica|Entrada||
|Estado Civil|Soltero/Casado/Divorciado/Viudo|Categórica|Entrada||
|Hijos|Número de hijos|Numérica|Entrada||
|Tipo Trabajo|Dependiente / Independiente / Freelancer / Empresario|Categórica|Entrada||
|Sueldo|Ingreso mensual en soles (PEN)|Numérica|Entrada||
|Deuda|Deuda total acumulada (PEN)|Numérica|Entrada||
|Historial Pago|Puntual / Atrasado / Moroso|Categórica|Entrada||
|Score|Puntaje crediticio|Numérica|Referencia||
|Riesgo|Alto / Bajo / Medio (variable objetivo)|Categórica|Salida (y)||
|Segmento Cliente|Regular / VIP / Premium|Categórica|Referencia||

La variable objetivo es "Riesgo", con tres clases: Alto, Bajo y Medio. Las variables predictoras utilizadas para el modelo son: Edad, Provincia, Estado Civil, Hijos, Tipo Trabajo, Sueldo, Deuda e Historial Pago [6].

**III. METODOLOGÍA**

La metodología adoptada sigue el estándar CRISP-DM (Cross Industry Standard Process for Data Mining), ampliamente utilizado en proyectos de ciencia de datos y Machine Learning aplicados al sector financiero [7]. Este marco organiza el proceso en seis fases iterativas: comprensión del negocio, comprensión de los datos, preparación de los datos, modelado, evaluación y despliegue. A continuación, se describen los doce pasos de implementación agrupados bajo cada fase CRISP-DM.

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.003.png)

*Ilustración *2*. Flujo de trabajo y fases del proceso metodológico adaptado de CRISP-DM*

***Fase 1: Comprensión del Negocio***

El objetivo principal es desarrollar un modelo de predicción de riesgo crediticio que clasifique a los clientes en tres categorías (Alto, Bajo y Medio) a partir de sus variables socioeconómicas. Esta fase define la pregunta de investigación: ¿En qué medida un modelo de Árbol de Decisión puede predecir el nivel de riesgo crediticio de un cliente? El éxito del modelo se medirá mediante la métrica de exactitud (accuracy) sobre el conjunto de prueba.

***Fase 2: Comprensión de los Datos***

Se exploró el dataset bancario peruano “data Banco F.xlsx” compuesto por 26000 registros de clientes con 12 variables (ver Tabla I). Se verificó la estructura de los datos con df.head(), identificando variables categóricas y numéricas, la variable objetivo “Riesgo” y la presencia de desbalance entre las clases Alto, Bajo y Medio.

***Fase 3: Preparación de los Datos***

Esta fase comprende los pasos de importación de librerías, carga del archivo, preprocesamiento y separación de variables, detallados a continuación.

***A. Importación de librerías***

Se importaron las librerías pandas (manejo de datos), train\_test\_split (división de datos), DecisionTreeClassifier (modelo), accuracy\_score (evaluación) y LabelEncoder (preprocesamiento categórico):

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.004.png)

*Ilustración *3*. Importación de librerías en Python.*

***B. Subir y leer archivo***

El archivo Excel fue cargado desde el computador local a Google Colab mediante files.upload() y leído con pd.read\_excel():

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.005.png)

*Ilustración *4*. Carga del archivo data banco.xlsx a Google Colab.*

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.006.png)

*Ilustración *5*. 4. Lectura del archivo con pandas.*

***C. Exploración de datos***

Se visualizaron las primeras cinco filas del dataset con df.head() para verificar la estructura de las columnas y los tipos de datos: 

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.007.png)

*Ilustración *6*. Vista previa de los datos con df.head().*

***D. Preprocesamiento***

Las variables categóricas (Provincia, Estado Civil, Tipo Trabajo, Historial Pago y Riesgo) fueron transformadas a valores numéricos utilizando LabelEncoder, requerimiento del algoritmo de Árbol de Decisión [8]:

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.008.png)

*Ilustración *7*. Codificación de variables categóricas con LabelEncoder.*

***E. Separación de variables y división del dataset***

Se definió X (variables predictoras: Edad, Provincia, Estado Civil, Hijos, Tipo Trabajo, Sueldo, Deuda, Historial Pago) e y (variable objetivo: Riesgo). El dataset fue dividido 80% entrenamiento / 20% prueba:

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.009.png)

*Ilustración *8*. Separación de variables predictoras (X) y objetivo (y)*

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.010.png)

*Ilustración *9*. División 80/20 con train\_test\_split*

***Fase 4: Modelado***

Se seleccionó el algoritmo DecisionTreeClassifier de scikit-learn por su interpretabilidad y adecuación al problema de clasificación multiclase. El modelo fue instanciado con parámetros por defecto y entrenado sobre el conjunto de entrenamiento (80% de los datos).

***F. Creación y entrenamiento del modelo***

Se instanció DecisionTreeClassifier() y el modelo fue entrenado con modelo.fit(X\_train, y\_train), aprendiendo los patrones que relacionan las variables con el nivel de riesgo [9]:

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.011.png)

*Ilustración *10*. Creación del modelo de Árbol de Decisión.*

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.012.png)

*Ilustración *11*. Entrenamiento del modelo.*

***Fase 5: Evaluación***

El modelo fue evaluado sobre el conjunto de prueba (20%) utilizando la métrica accuracy\_score. Adicionalmente, se realizó una prueba con un cliente nuevo para verificar la funcionalidad del modelo como herramienta de apoyo a decisiones financieras.

***G. Predicción y evaluación***

El modelo generó predicciones sobre el conjunto de prueba y se calculó la exactitud (accuracy) con accuracy\_score:

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.013.png)

*Ilustración *12*. Predicción sobre datos de prueba.*

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.014.png)

*Ilustración *13*. Exactitud obtenida: 0.92 (92%).*

***Fase 6: Despliegue***

El modelo entrenado fue puesto en uso mediante una prueba funcional con datos de un cliente nuevo, simulando su integración como herramienta de apoyo a la decisión crediticia. En un escenario real, este modelo podría desplegarse como API o componente de un sistema de evaluación financiera automatizada.

***H. Prueba con nuevo cliente***

Se realizó una prueba con un cliente nuevo ingresando sus datos directamente como vector numérico. El modelo predijo la categoría [0] que, según el mapeo de LabelEncoder (classes\_: ['Alto' 'Bajo' 'Medio']), corresponde a riesgo Alto:

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.015.png)

*Ilustración *14*. Comenzando las pruebas de clientes.*

![](Aspose.Words.43511ebc-2245-49a5-9f28-3b9e0e4816ae.016.png)

*Ilustración *15*. Predicción de riesgo para cliente nuevo: Alto.*

***I. Distribución del riesgo crediticio***

Se generó un gráfico de barras para visualizar la distribución de las clases de riesgo en el dataset. Se utilizó df["Riesgo"].value\_counts() para contabilizar los registros por categoría y le.inverse\_transform() para convertir los valores numéricos a etiquetas de texto. El gráfico evidencia un marcado desbalance de clases (ver Fig. 14 en sección IV), donde la mayoría de clientes pertenece a la categoría Alto, lo que constituye una limitación importante a considerar en la interpretación del modelo.

**IV. RESULTADOS Y DISCUSIÓN**

El modelo de Árbol de Decisión obtuvo una exactitud global de 92% sobre el conjunto de prueba, demostrando un alto nivel de precisión en la clasificación del riesgo crediticio de los clientes. Este resultado evidencia que el modelo logra identificar correctamente aproximadamente 92 de cada 100 casos evaluados, mostrando un desempeño eficiente sobre datos bancarios reales [2].

***Tabla ***2***. Resumen de resultados del modelo***

|Aspecto|Valor / Resultado|
| :-: | :-: |
|**Algoritmo**|DecisionTreeClassifier (scikit-learn)|
|**Total de registros**|26000 clientes|
|**División entrenamiento/prueba**|80% / 20% (20800 / 5200 registros)|
|**Variables predictoras (X)**|8 variables (Edad, Provincia, Estado Civil, Hijos, Tipo Trabajo, Sueldo, Deuda, Historial Pago)|
|**Variable objetivo (y)**|Riesgo: Alto / Bajo / Medio|
|**Exactitud (Accuracy)**|0\.92 (92%)|
|**Predicción cliente nuevo**|Riesgo Alto (clase [0])|

La exactitud alcanzada demuestra que el Árbol de Decisión fue capaz de aprender adecuadamente los patrones existentes dentro del dataset bancario utilizado. El rendimiento obtenido está relacionado con la calidad y consistencia de la información empleada, así como con la adecuada selección de variables predictoras relacionadas al comportamiento financiero de los clientes [1].

***Tabla ***3***. Comparación teórica de algoritmos de Machine Learning aplicados al riesgo crediticio.***

|Algoritmo|Precisión reportada en la literatura|Interpretabilidad|Complejidad|
| - | - | - | - |
|**Árbol de Decisión**|80% - 92%|Alta|Baja|
|**Regresión Logística**|75% - 88%|Alta|Baja|
|**Random Forest**|85% - 95%|Media|Media|
|**Gradient Boosting**|88% - 96%|Media|Alta|
|**XGBoost**|90% - 98%|Baja|Alta|


La Tabla 3 presenta una comparación de los algoritmos más utilizados en problemas de predicción de riesgo crediticio. Diversos estudios reportan que modelos de ensamble como Random Forest, Gradient Boosting y XGBoost suelen alcanzar niveles de precisión superiores a los obtenidos por algoritmos tradicionales, debido a su capacidad para capturar relaciones complejas entre las variables y reducir los errores de clasificación [10]. Sin embargo, estos modelos requieren una mayor capacidad computacional y presentan menor facilidad para interpretar las decisiones generadas.

Por otro lado, la Regresión Logística continúa siendo una técnica ampliamente utilizada en sistemas de credit scoring debido a su simplicidad y facilidad de implementación. No obstante, su capacidad predictiva puede verse limitada cuando existen relaciones no lineales entre las variables o patrones complejos en los datos [1].

En el presente estudio se seleccionó el algoritmo Árbol de Decisión debido a que combina un desempeño satisfactorio con una alta interpretabilidad. La exactitud obtenida de 92% se encuentra dentro de los valores reportados por investigaciones recientes y demuestra que el modelo es capaz de clasificar correctamente la mayoría de los casos analizados. Además, permite representar visualmente las reglas de decisión utilizadas para clasificar a los clientes según su nivel de riesgo, característica especialmente valorada en el sector financiero por motivos de transparencia y trazabilidad [4].

El dataset presenta desbalance de clases entre las categorías Alto, Bajo y Medio. Este fenómeno, documentado ampliamente en la literatura de credit scoring [5], hace que el modelo tienda a aprender mejor las clases mayoritarias. La Fig. 14 muestra la distribución de clientes según su nivel de riesgo: la categoría Alto concentra aproximadamente 16 200 clientes (62%), Medio alrededor de 7 500 (29%) y Bajo cerca de 2 400 (9%). Futuras investigaciones podrían aplicar técnicas de balanceo como SMOTE o ajuste de pesos de clase para mejorar el desempeño sobre las categorías minoritarias.

Asimismo, aunque algoritmos como Random Forest, Gradient Boosting y XGBoost pueden alcanzar mayores niveles de precisión, el Árbol de Decisión ofrece un equilibrio adecuado entre rendimiento, simplicidad e interpretabilidad. Esta ventaja resulta relevante cuando el objetivo no solo es predecir el riesgo crediticio, sino también comprender los factores que influyen en la clasificación y justificar las decisiones tomadas por el modelo.

La prueba realizada con un cliente nuevo (30 años, provincia codificada como 2, estado civil 1, dos hijos, tipo de trabajo 0, sueldo S/ 5 000, deuda S/ 8 000 e historial de pago 1) arrojó una predicción de riesgo Alto. Este resultado es coherente con el perfil financiero evaluado y demuestra la capacidad práctica del modelo para apoyar procesos de evaluación crediticia en entornos reales [3].

En términos generales, los resultados obtenidos permiten concluir que el Árbol de Decisión constituye una alternativa eficiente para la predicción del riesgo crediticio, no solo por su precisión del 92%, sino también por la claridad de sus reglas de clasificación y su facilidad de implementación. Estas características lo convierten en una herramienta adecuada para sistemas de apoyo a la toma de decisiones financieras, especialmente en contextos donde la interpretabilidad del modelo es tan importante como su capacidad predictiva.

**V. CONCLUSIONES**

El presente trabajo desarrolló y evaluó un modelo de predicción de riesgo crediticio basado en el algoritmo de Árbol de Decisión, implementado en Python con scikit-learn sobre un dataset bancario peruano real. Los hallazgos principales son:

El modelo alcanzó una exactitud global del 92% sobre el conjunto de prueba, evidenciando un desempeño satisfactorio en la clasificación de clientes según su nivel de riesgo crediticio (Alto, Bajo y Medio) [2].

El desbalance de clases representa uno de los principales desafíos en modelos de credit scoring, ya que puede afectar la capacidad predictiva sobre clases minoritarias [5]. El análisis de distribución del dataset reveló que el 62% de los clientes pertenece a la categoría Alto, el 29% a Medio y el 9% a Bajo, lo que explica la tendencia del modelo a predecir con mayor precisión la clase mayoritaria. Como trabajo futuro, se propone aplicar técnicas de balanceo como SMOTE y ajuste de hiperparámetros del árbol (max\_depth, min\_samples\_split) para mejorar aún más la precisión y capacidad de generalización del modelo.

La prueba con un cliente nuevo confirmó la funcionalidad del modelo como herramienta de apoyo a la toma de decisiones financieras, clasificando el perfil evaluado como riesgo Alto, resultado coherente con sus variables socioeconómicas y comportamiento financiero [3].

Finalmente, se propone comparar el Árbol de Decisión con modelos de ensemble como Random Forest, Gradient Boosting y XGBoost, así como incorporar técnicas modernas de interpretabilidad como valores de Shapley y LIME, las cuales han demostrado mejorar significativamente la explicabilidad de modelos complejos en sistemas de evaluación crediticia [6].

**REFERENCIAS**

[1]   Dastile, X., Celik, T., & Potsane, M. (2020). Statistical and machine learning models in credit scoring: A systematic literature survey. Applied Soft Computing, 91, 106263. https://doi.org/10.1016/j.asoc.2020.106263

[2]   Ayari, H., Guetari, P. R., & Kraïem, P. N. (2025). Machine learning powered financial credit scoring: a systematic literature review. Artificial Intelligence Review, 59(1). https://doi.org/10.1007/s10462-025-11416-2

[3]   Ugarte Chacon, D., Lee, S., & Park, J. (2025). An explainable machine learning model for consumer credit scoring in Mexico. Emerging Markets Review, 71, 101424. https://doi.org/10.1016/j.ememar.2025.101424

[4]   Valdrighi, G., et al. (2025). Best practices for responsible machine learning in credit scoring. Neural Computing and Applications, 37(25), 20781–20821. https://doi.org/10.1007/s00521-025-11520-y

[5]   Pereira, A. F. P., & Ashofteh, A. (2026). The Main Challenges of Machine Learning for Credit Scoring: A Review. In Lecture Notes in Networks and Systems (pp. 497–512). https://doi.org/10.1007/978-3-032-12879-9\_45

[6]   Chen, Y., Calabrese, R., & Martin-Barragan, B. (2024). JointLIME: An interpretation method for machine learning survival models with endogenous time-varying covariates in credit scoring. Risk Analysis, 45(12), 4135–4156. https://doi.org/10.1111/risa.17679

[7]   Mestiri, S. (2024). Credit scoring using machine learning and deep learning-based models. Data Science in Finance and Economics, 4(2), 236–248. https://doi.org/10.3934/DSFE.2024009

[8]   Bhatore, S., Mohan, L., & Reddy, Y. R. (2020). Machine learning techniques for credit risk evaluation: a systematic literature review. Journal of Banking and Financial Technology, 4, 111–138.

[9]   Louzada, F., Ara, A., & Fernandes, G. B. (2022). Machine learning-driven credit risk: a systemic review. Neural Computing and Applications. https://doi.org/10.1007/s00521-022-07472-2

[10]   Almutairi, A. N. (2022). Dynamic Effectiveness of Random Forest Algorithm in Financial Credit Risk Management. Ingénierie des Systèmes d'Information, 27(5). https://doi.org/10.18280/isi.270515
