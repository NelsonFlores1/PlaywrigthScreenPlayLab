# 🎭 PlaywrightScreenPlayLab

Proyecto de automatización de pruebas E2E para **ParaBank** utilizando **Playwright + Python + Gradle + Screenplay Pattern + Allure Reports**, con escenarios BDD escritos en **Gherkin en español**.

---

## 📋 Descripción

Framework de pruebas automatizadas que implementa el **Screenplay Pattern** — un enfoque centrado en el Actor que mejora la legibilidad, reutilización y mantenibilidad del código de pruebas. Los escenarios están definidos en español usando Gherkin (BDD) y se ejecutan contra la aplicación web [ParaBank](https://parabank.parasoft.com/).

Los **3 escenarios de prueba pasan** contra el sitio live de ParaBank:
- Registro de usuario y apertura de cuenta
- Transferencia de fondos entre cuentas
- Consulta de historial de transacciones

---

## ✅ Prerrequisitos

| Herramienta | Versión mínima | Descripción |
|---|---|---|
| Python | 3.11+ | Intérprete de Python |
| Java (JDK) | 11+ | Requerido para Gradle |
| Gradle | 7.x+ | Orquestador de tareas |
| Allure CLI | 2.x | Generación de reportes visuales |

### Instalación de Prerrequisitos

#### Python 3.11+

<details>
<summary><strong>🪟 Windows</strong></summary>

```bash
# Opción 1: winget
winget install Python.Python.3.11

# Opción 2: Descargar desde https://www.python.org/downloads/
# Marcar "Add python.exe to PATH" durante la instalación
```
</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

```bash
# Con Homebrew
brew install python@3.11

# O descargar desde https://www.python.org/downloads/
```
</details>

```bash
# Verificar instalación
python --version
```

#### Java JDK 11+

<details>
<summary><strong>🪟 Windows</strong></summary>

```bash
# Opción 1: winget
winget install EclipseAdoptium.Temurin.11.JDK

# Opción 2: Descargar desde https://adoptium.net/
```
</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

```bash
# Con Homebrew
brew install openjdk@11

# Agregar al PATH
echo 'export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
</details>

```bash
# Verificar
java -version
```

#### Gradle 7.x+

<details>
<summary><strong>🪟 Windows</strong></summary>

```bash
# Opción 1: Scoop
scoop install gradle

# Opción 2: Chocolatey
choco install gradle

# Opción 3: Descarga manual desde https://gradle.org/releases/
```
</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

```bash
# Con Homebrew
brew install gradle
```
</details>

```bash
# Verificar
gradle --version
```

#### Allure CLI 2.x

<details>
<summary><strong>🪟 Windows</strong></summary>

```bash
# Opción 1: Scoop
scoop install allure

# Opción 2: Chocolatey
choco install allure
```
</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

```bash
# Con Homebrew
brew install allure
```
</details>

```bash
# Verificar
allure --version
```

---

## 📁 Estructura del Proyecto

```
PlaywrightScreenPlayLab/
├── build.gradle                 # Orquestación Gradle (venv, deps, tests)
├── pytest.ini                   # Configuración pytest + Allure
├── requirements.txt             # Dependencias Python
├── conftest.py                  # Fixtures (browser, page, actor, screenshot on failure)
├── features/                    # Escenarios BDD en Gherkin (español)
│   ├── registro_usuario.feature
│   ├── transferencia_fondos.feature
│   └── historial_cuenta.feature
├── screenplay/                  # Patrón Screenplay
│   ├── actors/
│   │   ├── actor.py             # Clase Actor (attempts_to, asks_about)
│   │   └── browse_the_web.py    # Habilidad: navegar con Playwright
│   ├── tasks/                   # Tareas de alto nivel
│   │   ├── login.py
│   │   ├── register_user.py
│   │   ├── open_new_account.py
│   │   ├── transfer_funds.py
│   │   └── view_account_history.py
│   ├── interactions/            # Interacciones atómicas con la UI
│   │   ├── navigate_to.py
│   │   ├── fill_field.py
│   │   ├── click_element.py
│   │   ├── select_option.py
│   │   └── wait_for_selector.py
│   └── questions/               # Verificaciones del estado del sistema
│       ├── is_logged_in.py
│       ├── is_registration_successful.py
│       ├── is_transfer_successful.py
│       ├── is_transaction_history_visible.py
│       └── get_transactions.py
├── steps/                       # Step definitions (pytest-bdd)
│   ├── login_steps.py
│   ├── registro_steps.py
│   ├── transferencia_steps.py
│   ├── historial_steps.py
│   └── test_data_helper.py      # Generador de datos aleatorios
└── tests/                       # Test runners (wiring scenarios ↔ steps)
    ├── test_registro_usuario.py
    ├── test_transferencia_fondos.py
    └── test_historial_cuenta.py
```

---

## 🚀 Instalación y Ejecución

### Opción 1: Con Gradle (recomendado)

Gradle se encarga de **todo** automáticamente: crea el entorno virtual, instala dependencias Python, descarga Chromium y ejecuta las pruebas:

```bash
gradle test
```

**¿Qué hace internamente?**
1. `createVenv` — Crea un entorno virtual Python en `./venv/`
2. `installDependencies` — Instala las dependencias desde `requirements.txt`
3. `installPlaywright` — Descarga el navegador Chromium
4. `test` — Ejecuta pytest con reportes Allure

### Opción 2: Manual (paso a paso)

#### 1. Crear el entorno virtual (venv)

```bash
python -m venv venv
```

Esto crea un directorio `venv/` con un intérprete Python aislado.

#### 2. Activar el entorno virtual

```bash
# Windows (CMD)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

> Cuando el venv está activo, verás `(venv)` al inicio del prompt.

#### 3. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

Esto instala los siguientes componentes:

| Paquete | Versión | Propósito |
|---|---|---|
| `playwright` | >=1.40.0 | Motor de automatización del navegador |
| `pytest` | >=7.4.0 | Framework de testing |
| `pytest-bdd` | >=7.0.0 | Integración BDD con Gherkin |
| `pytest-playwright` | >=0.4.0 | Plugin Playwright para pytest |
| `allure-pytest` | >=2.13.0 | Generación de reportes Allure |
| `hypothesis` | >=6.90.0 | Testing basado en propiedades |

#### 4. Instalar navegador Chromium

```bash
playwright install chromium
```

Descarga el binario de Chromium que Playwright usará para ejecutar las pruebas.

#### 5. Ejecutar las pruebas

```bash
pytest tests/ -v --tb=short
```

### Opciones de ejecución adicionales

```bash
# Ejecutar en modo visible (ver el navegador)
pytest tests/ -v --headed

# Ejecutar solo un feature específico
pytest tests/test_transferencia_fondos.py -v

# Ejecutar con más detalle de errores
pytest tests/ -v --tb=long

# Desactivar el entorno virtual al terminar
deactivate
```

### 🖥️ Configuración del Modo del Navegador

Por defecto las pruebas se ejecutan en modo **headless** (sin ventana visible). Esto es ideal para CI/CD y ejecuciones rápidas. Para ver el navegador en acción, hay tres formas de activar el modo **headed**:

| Método | Comando / Configuración |
|---|---|
| Flag CLI | `pytest tests/ --headed` |
| Variable de entorno | `set HEADED=1` (Windows) / `export HEADED=1` (Linux/Mac) |
| Gradle (modificar build.gradle) | Agregar `'--headed'` al commandLine del task test |

**¿Cuándo usar cada modo?**

| Modo | Uso recomendado |
|---|---|
| **Headless** (por defecto) | CI/CD, ejecución en servidores, pipelines automáticos |
| **Headed** (visible) | Debugging, desarrollo de nuevos tests, demos |

**Ejemplo: ejecutar headed con variable de entorno (Windows)**
```bash
set HEADED=1
pytest tests/ -v
```

**Ejemplo: ejecutar headed con variable de entorno (Linux/Mac)**
```bash
HEADED=1 pytest tests/ -v
```

**Para configurarlo permanentemente en Gradle**, editar `build.gradle`:
```groovy
// Cambiar esta línea en el task test para agregar --headed
commandLine pythonExecutable, '-m', 'pytest', 'tests/',
    '-v',
    '--tb=short',
    '--alluredir=allure-results',
    '--headed'  // ← agregar esto para modo visible
```

> **Nota:** El modo headed es más lento porque renderiza la UI. Para pipelines de CI siempre usa headless (el valor por defecto).

### 📸 Configuración de Screenshots (Evidencias)

Por defecto, el framework captura un screenshot al **final de cada test** (pase o falle) y lo adjunta al reporte Allure. Puedes cambiar este comportamiento para capturar solo cuando falla:

| Modo | Comportamiento | Comando |
|---|---|---|
| `always` (por defecto) | Screenshot en cada test (pass + fail) | `pytest tests/` |
| `on-failure` | Screenshot solo cuando el test falla | `pytest tests/ --screenshot-mode=on-failure` |

**Con variable de entorno:**
```bash
# Windows
set SCREENSHOT_MODE=on-failure
pytest tests/ -v

# macOS / Linux
SCREENSHOT_MODE=on-failure pytest tests/ -v
```

**Para configurarlo permanentemente en `pytest.ini`:**
```ini
[pytest]
addopts = --alluredir=allure-results --screenshot-mode=on-failure
```

En el reporte Allure, los screenshots aparecen como adjuntos con nombre:
- `screenshot_NOMBRE_TEST_PASSED` — cuando el test pasó
- `screenshot_NOMBRE_TEST_FAILED` — cuando el test falló

### Manejo del Entorno Virtual (venv)

| Acción | Comando |
|---|---|
| Crear | `python -m venv venv` |
| Activar (Windows CMD) | `venv\Scripts\activate.bat` |
| Activar (PowerShell) | `venv\Scripts\Activate.ps1` |
| Activar (Linux/Mac) | `source venv/bin/activate` |
| Desactivar | `deactivate` |
| Recrear (si hay problemas) | Eliminar `venv/` y volver a crear |
| Actualizar dependencias | `pip install -r requirements.txt --upgrade` |

> **Nota:** El directorio `venv/` está excluido del repositorio via `.gitignore`. Cada desarrollador debe crear su propio entorno virtual.

---

## 📊 Reportes Allure

Los resultados se almacenan automáticamente en `allure-results/` (configurado en `pytest.ini`). Para visualizar:

```bash
# Servidor temporal con reporte interactivo
allure serve allure-results

# O generar reporte estático
allure generate allure-results -o allure-report --clean
allure open allure-report
```

El reporte incluye:
- Pasos detallados de cada escenario (gracias a `with allure.step(...)`)
- Screenshots automáticos al final de cada test (configurable a solo en fallos con `--screenshot-mode=on-failure`)
- Historial de ejecuciones y estadísticas

---

## 🏗️ Arquitectura: Screenplay Pattern

El código se organiza en torno a un **Actor** que ejecuta **Tareas** mediante **Interacciones** y valida resultados a través de **Preguntas**:

```
Actor → Tarea → Interacción(es)
  └──→ Pregunta → Verificación
```

### Componentes

| Capa | Responsabilidad | Ejemplo |
|---|---|---|
| **Actor** | Representa al usuario que interactúa con el sistema | `Actor(BrowseTheWeb(page))` |
| **Task** | Acción de alto nivel con significado de negocio | `Login(username, password)` |
| **Interaction** | Acción atómica sobre la UI | `FillField(selector, value)` |
| **Question** | Consulta sobre el estado actual del sistema | `IsLoggedIn()` |
| **Ability** | Capacidad del actor para interactuar | `BrowseTheWeb(page)` |

### Integración con Allure

Cada Task e Interaction reporta sus acciones a Allure usando el context manager:

```python
class Login:
    def perform_as(self, actor) -> None:
        with allure.step(f"Login as {self._username}"):
            actor.attempts_to(
                FillField(self.USERNAME_INPUT, self._username),
                FillField(self.PASSWORD_INPUT, self._password),
                ClickElement(self.LOGIN_BUTTON),
            )
```

Este patrón genera un árbol jerárquico de pasos en el reporte, donde cada Tarea contiene sub-pasos con las Interacciones ejecutadas.

### Flujo de una prueba

```python
# El actor ejecuta una tarea
actor.attempts_to(Login("john", "demo"))

# El actor verifica el resultado
assert actor.asks_about(IsLoggedIn())
```

---

## 🥒 Escenarios BDD (Gherkin en Español)

```gherkin
# language: es
Característica: Transferencia de fondos

Antecedentes:
  Dado el usuario se encuentra en la página de login de ParaBank
  Cuando ingresa el usuario "john" y la contraseña "demo"
  Entonces el sistema muestra el dashboard de la cuenta

Escenario: Transferir dinero entre cuentas exitosamente
  Cuando el usuario navega a la opción "Transfer Funds"
  Y selecciona la cuenta origen
  Y selecciona la cuenta destino
  Y ingresa un monto válido "100"
  Y confirma la transferencia
  Entonces el sistema muestra el mensaje de transferencia exitosa
```

> **Nota:** Se usa el usuario `john/demo` (credenciales por defecto de ParaBank). El framework inicializa automáticamente la base de datos de ParaBank al iniciar cada sesión de tests para garantizar que los usuarios y cuentas existan.

---

## 📝 Features (Funcionalidades)

### 1. Registro de Usuario (`registro_usuario.feature`)
Registra un nuevo usuario con datos generados aleatoriamente y abre una cuenta CHECKING. Este escenario sirve como **setup** para los demás tests.

### 2. Transferencia de Fondos (`transferencia_fondos.feature`)
Valida la transferencia exitosa de fondos entre dos cuentas, verificando el mensaje de confirmación "Transfer Complete".

### 3. Historial de Cuenta (`historial_cuenta.feature`)
Verifica que el usuario puede consultar el historial de transacciones y que cada movimiento tiene fecha y descripción.

---

## 🔗 Cómo se Enlaza un Feature con el Proyecto

El framework conecta los archivos mediante esta cadena:

```
pytest.ini
  ├── testpaths = tests/                  ← Dónde buscar tests
  └── bdd_features_base_dir = features/   ← Dónde buscar .feature files

tests/test_XXX.py (Test Runner)
  ├── scenarios("XXX.feature")            ← Enlaza al feature file
  ├── from steps.login_steps import *     ← Steps compartidos
  └── from steps.XXX_steps import *       ← Steps específicos

steps/XXX_steps.py (Step Definitions)
  ├── @when("texto exacto del paso")      ← Debe coincidir con el .feature
  └── actor.attempts_to(Task)             ← Delega al Screenplay Pattern

conftest.py (Fixtures automáticas)
  └── actor fixture                       ← Se inyecta automáticamente
```

**Para agregar un nuevo escenario**, consulta la guía detallada: [`GUIA_AGREGAR_ESCENARIO.md`](GUIA_AGREGAR_ESCENARIO.md)

---

## 🛠️ Tecnologías

- **Playwright** — Automatización de navegador (Chromium)
- **pytest** — Framework de pruebas
- **pytest-bdd** — Soporte BDD con Gherkin
- **Allure** — Reportes visuales e interactivos
- **Gradle** — Orquestación de build y ejecución
- **Hypothesis** — Testing basado en propiedades (disponible)

---