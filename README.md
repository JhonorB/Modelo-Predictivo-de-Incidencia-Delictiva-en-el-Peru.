# 🏛️ SIDPOL — Sistema Inteligente de Predicción de Incidencia Delictiva

**Machine Learning Supervisado + Microservicios** para la proyección de incidencia delictiva a nivel departamental en el Perú. Desarrollado bajo la metodología **CRISP-DM** con **Random Forest Regressor + SMOTE**.

> **⚠️ IMPORTANTE PARA USUARIOS WINDOWS:** Este README incluye instrucciones específicas para Windows (PowerShell / Git Bash). Se asume que usas **Docker Desktop con WSL2 backend**. Cada sección marca las diferencias entre SO.

---

## 📋 Tabla de Contenidos

- [Arquitectura](#-arquitectura)
- [Stack Tecnológico](#-stack-tecnológico)
- [Prerrequisitos (Windows & Linux)](#-prerrequisitos-windows--linux)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Guía Rápida de Ejecución](#-guía-rápida-de-ejecución)
- [1. Motor de IA (FastAPI + Python)](#1-motor-de-ia-fastapi--python)
- [2. Docker (Base de Datos MySQL)](#2-docker-base-de-datos-mysql)
- [3. Backend (Spring Boot + Maven)](#3-backend-spring-boot--maven)
- [4. Frontend (Angular)](#4-frontend-angular)
- [API Endpoints](#-api-endpoints)
- [Solución de Problemas Comunes (Windows)](#-solución-de-problemas-comunes-en-windows)
- [Variables de Entorno](#-variables-de-entorno)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│              sidpol-frontend (Angular 21)                    │
│              http://localhost:4200                           │
│         Login | Dashboard | Predicciones                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP con JWT (Bearer token)
┌──────────────────────────▼──────────────────────────────────┐
│              sidpol-backend (Spring Boot 3.5 / Java 17)      │
│  ┌────────────┐  ┌──────────────┐  ┌───────────────────┐    │
│  │ Auth       │  │ Predicción   │  │ Usuario           │    │
│  │ /api/auth  │  │ /api/predicciones │ /api/usuarios   │    │
│  └─────┬──────┘  └──────┬───────┘  └───────────────────┘    │
│        │                │                                     │
│  ┌─────▼────────────────▼────────────────────────────────┐   │
│  │  MotorIaService → http://localhost:8000/api/v1/...    │   │
│  └───────────────────────────────────────────────────────┘   │
│                    │ JDBC (MySQL)                             │
│          ┌─────────▼──────────┐                              │
│          │  MySQL 8.0         │                              │
│          │  sidpoldb          │                              │
│          │  localhost:3306    │                              │
│          └────────────────────┘                              │
└──────────────────────────────┬───────────────────────────────┘
                               │ POST /predict/incidencia
┌──────────────────────────────▼───────────────────────────────┐
│     motor_Sidpol (FastAPI + Python 3.11)                     │
│  ┌────────────┐  ┌────────────────┐  ┌───────────────────┐  │
│  │ /health    │  │ /predict/      │  │ /model/metrics    │  │
│  │ (GET)      │  │ incidencia(POST)│  │ (GET)            │  │
│  └────────────┘  └───────┬────────┘  └───────────────────┘  │
│                          │ joblib.load()                      │
│               ┌──────────▼──────────┐                        │
│               │  pipeline_sidpol.pkl │                        │
│               │  (Random Forest +   │                        │
│               │   OneHotEncoder)    │                        │
│               └─────────────────────┘                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Puerto | Windows |
|-------------|-----------|--------|---------|
| **Frontend** | Angular 21, TypeScript, SCSS, Plotly.js, Chart.js | `4200` | ✅ Nativo |
| **Backend** | Java 17+, Spring Boot 3.5, Maven, Spring Security + JWT | `8080` | ✅ Nativo |
| **Motor IA** | Python 3.11+, FastAPI, Uvicorn, Scikit-Learn, Pandas, joblib | `8000` | ✅ Nativo o Docker |
| **Base de Datos** | MySQL 8.0 (contenedor Docker) | `3306` | 🐳 Docker obligatorio |
| **Orquestación** | Docker Compose | — | 🐳 Docker Desktop |

---

## 📋 Prerrequisitos (Windows & Linux)

### 🔹 Para todos los usuarios

| Herramienta | Versión Mínima | Windows (Descarga) | Linux |
|-------------|---------------|-------------------|-------|
| **Docker Desktop** | 4.x | [docker.com](https://www.docker.com/products/docker-desktop/) | `sudo apt install docker.io docker-compose-v2` |
| **Git** | 2.x | [git-scm.com](https://git-scm.com/download/win) | `sudo apt install git` |
| **Java (JDK)** | 17+ | [Adoptium Temurin 17](https://adoptium.net/temurin/releases/?version=17) | `sudo apt install openjdk-17-jdk` |
| **Maven** | 3.8+ | `winget install Apache.Maven` o [manual](https://maven.apache.org/download.cgi) | `sudo apt install maven` |
| **Node.js** | 20+ | [nodejs.org](https://nodejs.org/) (versión LTS) | `sudo apt install nodejs npm` |
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) | `sudo apt install python3 python3-pip python3-venv` |

### 🔹 Verificar instalaciones

Abre una terminal (**PowerShell** en Windows, **bash** en Linux) y ejecuta:

```powershell
# Windows (PowerShell) - Verificar todo:
docker --version
java -version
mvn --version
node --version
npm --version
python --version
pip --version
git --version
```

```bash
# Linux - Verificar todo:
docker --version && java -version && mvn --version && node --version && npm --version && python3 --version && pip3 --version && git --version
```

> **⚠️ En Windows:** Si `python` no funciona, usa `py` o `python3`. Marca la opción **"Add Python to PATH"** durante la instalación.

### 🔹 Configurar Docker Desktop en Windows

1. Instala [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Abre Docker Desktop → Settings → General → ✅ **Use WSL 2 based engine**
3. Ve a Settings → Resources → WSL Integration → Activa tu distro WSL
4. Aplica y reinicia Docker Desktop
5. Verifica: `docker run hello-world`

> **Alternativa:** Si no puedes usar Docker, salta a la [Sección 1b — Motor IA sin Docker](#1b-ejecutar-el-motor-de-ia-sin-docker-windowslinux) y usa **MySQL portable** o [XAMPP](https://www.apachefriends.org/).

---

## 📁 Estructura del Proyecto

```
📦 DATA_PROYEC/
├── 📂 motor_Sidpol/                 # 🧠 Motor de IA (Python)
│   ├── 📄 app.py                    #    API REST FastAPI (inferencia)
│   ├── 📄 script_modelo_sidpol.py   #    Entrenamiento del modelo ML
│   ├── 📄 pipeline_sidpol.pkl       #    Modelo entrenado (Random Forest)
│   ├── 📄 Base_datos_SIDPOL_Marzo2026.xlsx  # Dataset (.xlsx)
│   ├── 📄 metricas_sidpol.json      #    Métricas de rendimiento
│   ├── 📄 graficos_sidpol.json      #    Gráficos Plotly JSON
│   ├── 📄 requirements.txt          #    Dependencias Python
│   ├── 📄 Dockerfile                #    Imagen Docker del motor IA
│   └── 📄 docker-compose.yml        #    Orquestación IA + MySQL
│
├── 📂 sidpol-backend/               # ⚙️ Backend Spring Boot
│   ├── 📄 pom.xml                   #    Config Maven + dependencias
│   ├── 📄 mvnw / mvnw.cmd           #    Maven Wrapper (Windows .cmd)
│   └── 📂 src/main/java/com/utp/sidpol/sidpol_backend/
│       ├── 📂 controller/           #    Auth, Prediccion, Usuario
│       ├── 📂 service/              #    MotorIaService, UsuarioService
│       ├── 📂 security/             #    JWT + SecurityConfig
│       ├── 📂 entity/               #    Usuario, Rol (JPA)
│       ├── 📂 dto/                  #    Request/Response DTOs
│       └── 📂 repository/           #    JPA Repositories
│
├── 📂 sidpol-frontend/              # 🌐 Frontend Angular
│   ├── 📄 angular.json
│   ├── 📄 package.json
│   └── 📂 src/app/
│       ├── 📂 core/                 #    Guards, Interceptors, Services
│       └── 📂 features/
│           ├── 📂 auth/login/       #    Pantalla de inicio de sesión
│           ├── 📂 auth/registro/    #    Registro de usuario
│           └── 📂 dashboard/        #    Dashboard con gráficos Plotly
│
├── 📄 .gitignore
├── 📄 DOCUMENTACION_GENERAL.md
└── 📄 README.md                     # ← Este archivo
```

---

## 🚀 Guía Rápida de Ejecución

### Si usas Docker (recomendado en Windows):

```powershell
# 1. Clonar (si no lo tienes):
git clone https://github.com/JhonorB/Modelo-Predictivo-de-Incidencia-Delictiva-en-el-Peru
cd Modelo-Predictivo-de-Incidencia-Delictiva-en-el-Peru

# 2. Levantar MySQL + Motor IA con Docker:
cd motor_Sidpol
docker compose up --build -d

# 3. Verificar que ambos contenedores estén corriendo:
docker ps

# 4. En otra terminal, iniciar Backend:
cd ../sidpol-backend
.\mvnw.cmd spring-boot:run      # Windows PowerShell
# ./mvnw spring-boot:run        # Linux / Git Bash

# 5. En otra terminal, iniciar Frontend:
cd ../sidpol-frontend
npm install
ng serve -o
```

### Sin Docker (todo local):

```powershell
# 1. Instalar MySQL manual (o XAMPP) y crear DB "sidpoldb"

# 2. Iniciar Motor IA (Python):
cd motor_Sidpol
python -m venv venv
.\venv\Scripts\activate         # Windows
# source venv/bin/activate      # Linux
pip install -r requirements.txt
python app.py &

# 3. Iniciar Backend:
cd ../sidpol-backend
.\mvnw.cmd spring-boot:run

# 4. Iniciar Frontend:
cd ../sidpol-frontend
npm install
ng serve -o
```

---

## 1. Motor de IA (FastAPI + Python)

### 1a. Con Docker (RECOMENDADO)

```powershell
cd motor_Sidpol

# Construir imagen e iniciar contenedores en segundo plano:
docker compose up --build -d

# Verificar que estén corriendo:
docker ps
# Deberías ver 2 contenedores: mysql_sidpol_server y motor_sidpol_ia

# Ver logs del motor IA:
docker logs motor_sidpol_ia -f

# Probar que responde:
curl http://localhost:8000/api/v1/health
```

**Salida esperada:**
```json
{"estado":"OPERATIVO","microservicio":"SIDPOL Motor Predictivo IA","version":"4.0.0-Enterprise","estado_modelo_ram":true}
```

### 1b. Ejecutar el Motor de IA sin Docker (Windows/Linux)

```powershell
cd motor_Sidpol

# 1. Crear y activar entorno virtual:
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Si da error de permisos, ejecuta: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Windows (Git Bash):
source venv/Scripts/activate

# Linux/Mac:
source venv/bin/activate

# 2. Instalar todas las dependencias:
pip install --upgrade pip
pip install -r requirements.txt
```

**📦 Dependencias que se instalan (`requirements.txt`):**

| Paquete | Versión | Para qué sirve |
|---------|---------|---------------|
| `fastapi` | ≥0.100.0 | Framework REST API |
| `uvicorn[standard]` | ≥0.23.0 | Servidor ASGI para FastAPI |
| `pydantic` | ≥2.3.0 | Validación de datos (schemas) |
| `scikit-learn` | ≥1.3.0 | Random Forest, OneHotEncoder, métricas |
| `imbalanced-learn` | ≥0.11.0 | SMOTE (balanceo de clases) |
| `joblib` | ≥1.3.0 | Serialización/deserialización del modelo `.pkl` |
| `pandas` | ≥2.0.0 | Manipulación de datos (DataFrames) |
| `numpy` | ≥1.24.0 | Operaciones numéricas |
| `openpyxl` | ≥3.1.2 | Lectura de archivos Excel (.xlsx) |
| `matplotlib` | ≥3.7.0 | Gráficos estáticos (offline) |
| `seaborn` | ≥0.12.0 | Gráficos estadísticos |
| `plotly` | ≥5.18.0 | Gráficos interactivos JSON (→ Angular) |
| `python-dotenv` | ≥1.0.0 | Variables de entorno |

**Posibles errores en Windows y solución:**
```
ERROR: Error al instalar numpy (Falta Microsoft C++ Build Tools)
```
➡️ Descarga [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
○ Marca solo "Herramientas de compilación de C++" durante la instalación.

```
Falta archivo VCRUNTIME140.dll
```
➡️ Instala [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

### 1c. Entrenar el modelo (solo si falta `pipeline_sidpol.pkl`)

```powershell
# Con el entorno virtual activado:
cd motor_Sidpol
python script_modelo_sidpol.py
```

Esto generará: `pipeline_sidpol.pkl`, `metricas_sidpol.json`, `graficos_sidpol.json`

---

### 1d. Iniciar el servidor FastAPI (sin Docker)

```powershell
# Con el entorno virtual activado:
python app.py
# El servidor arranca en http://localhost:8000

# Deberías ver:
# 🚀 INICIANDO MOTOR PREDICTIVO SIDPOL v4.0.0-Enterprise
# ✅ Pipeline cargado exitosamente en X.XX ms
```

**Probar que funciona:**
```powershell
curl http://localhost:8000/api/v1/health
# O en PowerShell: Invoke-RestMethod -Uri http://localhost:8000/api/v1/health
```

**Documentación interactiva:**
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## 2. Docker (Base de Datos MySQL)

El archivo `docker-compose.yml` levanta **2 servicios**:

```yaml
services:
  db-sidpol:                    # MySQL 8.0
    image: mysql:8.0
    container_name: mysql_sidpol_server
    ports: ["3306:3306"]
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: sidpoldb
      MYSQL_USER: utp_admin
      MYSQL_PASSWORD: utp_password

  motor_ia:                     # Motor Python
    build: .
    container_name: motor_sidpol_ia
    ports: ["8000:8000"]
    depends_on: [db-sidpol]
```

### Comandos útiles de Docker para Windows:

```powershell
# Iniciar servicios:
cd motor_Sidpol
docker compose up --build -d

# Ver contenedores activos:
docker ps

# Ver logs en tiempo real:
docker compose logs -f

# Reiniciar un servicio específico:
docker compose restart motor_ia

# Detener servicios (sin borrar datos):
docker compose down

# Detener y borrar volúmenes (⚠️ borra la BD):
docker compose down -v

# Acceder a MySQL dentro del contenedor:
docker exec -it mysql_sidpol_server mysql -u utp_admin -p
# (contraseña: utp_password)

# Ejecutar un comando dentro del contenedor del motor IA:
docker exec -it motor_sidpol_ia bash
```

### Configurar MySQL nativo en Windows (alternativa sin Docker)

Si no puedes usar Docker, instala [MySQL Installer](https://dev.mysql.com/downloads/installer/) y crea la base de datos:

```sql
CREATE DATABASE sidpoldb;
CREATE USER 'utp_admin'@'localhost' IDENTIFIED BY 'utp_password';
GRANT ALL PRIVILEGES ON sidpoldb.* TO 'utp_admin'@'localhost';
FLUSH PRIVILEGES;
```

O usa [XAMPP](https://www.apachefriends.org/) (más simple) — solo activa MySQL desde el panel.

---

## 3. Backend (Spring Boot + Maven)

### Requisitos previos

- ✅ **MySQL corriendo** (via Docker o nativo), puerto `3306`
- ✅ Base de datos `sidpoldb` creada
- ✅ Java 17+ instalado (`java -version`)
- ✅ Maven instalado o usa `mvnw.cmd` (incluido)

### Ejecutar

```powershell
cd sidpol-backend

# Windows (PowerShell) — usando Maven Wrapper:
.\mvnw.cmd clean install -DskipTests
.\mvnw.cmd spring-boot:run

# Windows (Git Bash):
./mvnw clean install -DskipTests
./mvnw spring-boot:run

# Linux/Mac:
./mvnw clean install -DskipTests
./mvnw spring-boot:run

# Si tienes Maven instalado globalmente:
mvn clean install -DskipTests
mvn spring-boot:run
```

**Primera ejecución:** Maven descargará todas las dependencias automáticamente. Puede tomar 2-5 minutos.

**Salida esperada:**
```
Tomcat started on port 8080 (http)
Started Application in X.XXX seconds
```

**Verificar:**
```powershell
curl http://localhost:8080/api/auth/login
```

### Posibles errores en Windows:

| Error | Causa | Solución |
|-------|-------|----------|
| `No se reconoce 'JAVA_HOME'` | Java no está en PATH | Verifica con `java -version`. Si funciona, agrega `JAVA_HOME` como variable de sistema apuntando a `C:\Program Files\Eclipse Adoptium\jdk-17.0.x\` |
| `mvnw.cmd no se encuentra` | Estás en el directorio equivocado | Asegúrate de estar dentro de `sidpol-backend/` |
| `Port 8080 already in use` | Otro programa usa el puerto | Cierra el otro programa o cambia el puerto en `application.properties`: `server.port=8081` |
| `CommunicationsException: Connection refused` | MySQL no está corriendo | Inicia Docker: `docker compose up -d db-sidpol` desde `motor_Sidpol/` |

---

## 4. Frontend (Angular)

### Requisitos

- ✅ Node.js 20+ instalado
- ✅ Backend Spring Boot corriendo (para consumir APIs)

### Ejecutar

```powershell
cd sidpol-frontend

# 1. Instalar dependencias (solo la primera vez o cuando cambie package.json):
npm install

# 2. Iniciar servidor de desarrollo:
ng serve -o
```

**Salida esperada:**
```
✔ Browser application bundle generation complete.
✔ Initial chunk files | Names
Initial total: X.XX MB
- Build at: YYYY-MM-DDTHH:MM:SS.XXXZ - Hash: abc123...
✔ http://localhost:4200
```

**Esto abre automáticamente:** http://localhost:4200

### Notas para Windows:

- Si `ng serve -o` no abre el navegador, abre manualmente http://localhost:4200
- Si `ng` no se reconoce, usa `npx ng serve -o` o instala Angular CLI globalmente: `npm install -g @angular/cli`
- Si el puerto `4200` está ocupado, usa: `ng serve -o --port 4300`

### Credenciales por defecto (creadas automáticamente por `DataInitializer.java`):

| Rol | Usuario | Contraseña |
|-----|---------|-----------|
| **Admin** | `admin` | `admin123` |
| **Usuario** | `usuario` | `usuario123` |

---

## 🌐 API Endpoints

### Motor IA (`http://localhost:8000/api/v1`)

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| `GET` | `/health` | Estado del microservicio | ❌ No |
| `GET` | `/catalogos` | Departamentos y tipos de delito | ❌ No |
| `GET` | `/model/metrics` | Métricas del modelo (R², MAE, RMSE) | ❌ No |
| `GET` | `/model/graficos` | Gráficos Plotly del modelo | ❌ No |
| `POST` | `/predict/incidencia` | Predecir incidencia delictiva | ❌ No |

**Ejemplo de predicción:**
```powershell
# Windows PowerShell:
$body = @{
    anio = 2026
    mes = 7
    dpto_hecho_new = "LIMA METROPOLITANA"
    es_delito_x = "1.Delitos"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/v1/predict/incidencia -Method Post -Body $body -ContentType "application/json"
```

```bash
# Linux / Git Bash:
curl -X POST http://localhost:8000/api/v1/predict/incidencia \
  -H "Content-Type: application/json" \
  -d '{"anio":2026,"mes":7,"dpto_hecho_new":"LIMA METROPOLITANA","es_delito_x":"1.Delitos"}'
```

**Respuesta:**
```json
{
  "status": "EXITO",
  "prediccion_total_delitos": 1234.56,
  "nivel_alerta": "ALTO",
  "metadata_tecnica": {
    "tiempo_inferencia_modelo_ms": 2.34,
    "algoritmo": "RandomForestRegressor_Ensemble"
  },
  "mensaje_ejecutivo": "El modelo proyecta un volumen de 1235 denuncias por '1.Delitos' en la región de LIMA METROPOLITANA para el periodo 7/2026. Escenario de alerta: ALTO."
}
```

**Niveles de alerta:**
| Rango | Nivel |
|-------|-------|
| < 50 | 🟢 BAJO |
| 50–249 | 🟡 MEDIO |
| 250–799 | 🟠 ALTO |
| ≥ 800 | 🔴 CRÍTICO |

### Backend Spring Boot (`http://localhost:8080`)

| Método | Ruta | Descripción | Rol |
|--------|------|-------------|-----|
| `POST` | `/api/auth/login` | Iniciar sesión | público |
| `POST` | `/api/auth/register` | Registrar usuario | público |
| `POST` | `/api/predicciones/incidencia` | Predecir (consume motor IA) | ADMIN |
| `GET` | `/api/predicciones/catalogos` | Obtener catálogos | USER, ADMIN |
| `GET` | `/api/predicciones/model/metrics` | Métricas del modelo | ADMIN |
| `GET` | `/api/predicciones/model/graficos` | Gráficos del modelo | USER, ADMIN |
| `GET` | `/api/usuarios` | Listar usuarios | ADMIN |

**Login de ejemplo:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/api/auth/login -Method Post -Body '{"username":"admin","password":"admin123"}' -ContentType "application/json"
```

**Respuesta:** Incluye el token JWT que se usa en el header `Authorization: Bearer <token>`.

---

## 🐛 Solución de Problemas Comunes (en Windows)

### 🔸 Docker no funciona

```
Error: docker: command not found
```
➡️ Docker Desktop no está instalado o no está en PATH. Reinstálalo desde [docker.com](https://www.docker.com/products/docker-desktop/).

```
Error: Cannot connect to the Docker daemon
```
➡️ Docker Desktop no está corriendo. Ábrelo desde el menú Inicio.

```
Error: WSL 2 installation is incomplete
```
➡️ `wsl --install` en PowerShell como Administrador, luego reinicia.

### 🔸 Python / Entorno virtual

```
Error: 'pip' no se reconoce
```
➡️ Durante la instalación de Python, marca **"Add Python to PATH"**.
➡️ O usa `py -m pip install -r requirements.txt`

```
Error: Set-ExecutionPolicy restringe la ejecución de scripts
```
➡️ `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

```
Error: No module named 'numpy' (WSL2)
```
➡️ Activa el entorno virtual: `.\venv\Scripts\Activate.ps1`

### 🔸 Backend Spring Boot

```
Error: JAVA_HOME not set
```
➡️ En Windows, agrega variable del sistema:
   - Nombre: `JAVA_HOME`
   - Valor: `C:\Program Files\Eclipse Adoptium\jdk-17.0.12.7-hotspot` (o tu ruta de JDK 17)

```
Error: Port 8080 already in use
```
➡️ `netstat -ano | findstr :8080` → identifica el PID → `taskkill /PID <PID> /F`

### 🔸 Frontend Angular

```
Error: ng no se reconoce
```
➡️ `npm install -g @angular/cli`

```
Error: node_modules missing
```
➡️ `npm install`

```
Error: ERR_OSSL_EVP_UNSUPPORTED
```
➡️ `set NODE_OPTIONS=--openssl-legacy-provider` (PowerShell) y vuelve a ejecutar `ng serve`

### 🔸 Git (saltos de línea / line endings)

```powershell
# Si ves errores de CRLF/LF en Windows:
git config --global core.autocrlf true
git config --global core.eol crlf
```

### 🔸 Puertos ocupados

```powershell
# Ver qué está usando un puerto específico:
netstat -ano | findstr :3306
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :4200
```

---

## 🔐 Variables de Entorno

### Backend (`sidpol-backend/src/main/resources/application.properties`)

| Propiedad | Valor por defecto | Descripción |
|-----------|------------------|-------------|
| `spring.datasource.url` | `jdbc:mysql://127.0.0.1:3306/sidpoldb?createDatabaseIfNotExist=true&useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true` | Conexión MySQL |
| `spring.datasource.username` | `utp_admin` | Usuario BD |
| `spring.datasource.password` | `utp_password` | Contraseña BD |
| `spring.jpa.hibernate.ddl-auto` | `update` | Crear/actualizar tablas automáticamente |
| `jwt.secret` | `Cl4ve-S3creta-SIDPOL-2026-MegaUltraSegura-CambiarEnProduccion!` | Secreto JWT |
| `jwt.expiration` | `86400000` | 24h en milisegundos |

### Motor IA (variables de entorno del contenedor)

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `ENV` | `development` | Entorno de ejecución |

---

## ✅ Checklist para Windows — ¿Todo listo?

- [ ] Docker Desktop instalado y corriendo (con WSL2)
- [ ] Java 17+ instalado (`java -version`)
- [ ] Maven instalado (`mvn --version`)
- [ ] Node.js 20+ instalado (`node --version`)
- [ ] Python 3.11+ instalado (`python --version`)
- [ ] Puerto 3306, 8000, 8080, 4200 libres
- [ ] `docker compose up --build -d` desde `motor_Sidpol/`
- [ ] `docker ps` muestra 2 contenedores activos
- [ ] `curl http://localhost:8000/api/v1/health` responde `OPERATIVO`
- [ ] Backend Spring Boot iniciado (sin errores)
- [ ] Frontend Angular compilado sin errores

---

## 📚 Más información

- **Documentación general**: [DOCUMENTACION_GENERAL.md](./DOCUMENTACION_GENERAL.md)
- **Swagger Motor IA**: http://localhost:8000/api/v1/docs
- **Swagger Backend**: http://localhost:8080/swagger-ui.html (si está configurado)
- **Artículo científico**: [SIDPOL_Articulo_Actualizado.docx](./SIDPOL_Articulo_Actualizado.docx)

---

Desarrollado con ❤️ por **Jhon Ordoñez, Luis Angeles, Angel Leon, Jean Loa** — Universidad Tecnológica del Perú (UTP)

**Stack:** Python · FastAPI · Scikit-Learn · Java · Spring Boot · Angular · Docker · MySQL · JWT · Plotly
