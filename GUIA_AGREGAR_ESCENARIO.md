# 📘 Guía: Cómo Agregar un Nuevo Escenario

Esta guía explica paso a paso cómo agregar un nuevo escenario de prueba al proyecto siguiendo el Screenplay Pattern con Allure.

---

## Resumen de Pasos

1. Crear el archivo `.feature` (Gherkin en español)
2. Crear las Interactions necesarias (si no existen)
3. Crear el Task correspondiente
4. Crear las Questions necesarias
5. Crear los Step Definitions
6. Crear el Test Runner y enlazarlo al proyecto
7. Ejecutar y validar

---

## Ejemplo: Agregar escenario "Pago de Facturas"

Usaremos un ejemplo concreto para ilustrar cada paso.

---

## Paso 1: Crear el archivo Feature

Crear el archivo en `features/` con la extensión `.feature` y el tag `# language: es`:

**Archivo:** `features/pago_facturas.feature`

```gherkin
# language: es
Característica: Pago de facturas

Antecedentes:
  Dado el usuario se encuentra en la página de login de ParaBank
  Cuando ingresa el usuario "john" y la contraseña "demo"
  Entonces el sistema muestra el dashboard de la cuenta

Escenario: Pagar una factura exitosamente
  Cuando el usuario navega a la opción "Bill Pay"
  Y completa los datos del beneficiario
  Y ingresa el monto de la factura "50"
  Y confirma el pago
  Entonces el sistema muestra el mensaje de pago exitoso
```

> **Nota:** Se usan las credenciales por defecto de ParaBank (`john/demo`). El framework inicializa la base de datos automáticamente al inicio de cada sesión de tests.

---

## Paso 2: Crear Interactions (si se necesitan nuevas)

Revisa las Interactions existentes en `screenplay/interactions/`:
- `NavigateTo` — Navegar a una página
- `FillField` — Llenar un campo
- `ClickElement` — Hacer clic en un elemento
- `SelectOption` — Seleccionar una opción de dropdown
- `WaitForSelector` — Esperar a que un elemento sea visible

Si tu feature necesita una interacción que **no existe**, créala. Por ejemplo, si necesitas subir un archivo:

**Archivo:** `screenplay/interactions/upload_file.py`

```python
import allure


class UploadFile:
    """Upload a file to an input element."""

    def __init__(self, selector: str, file_path: str):
        self._selector = selector
        self._file_path = file_path

    def perform_as(self, actor) -> None:
        with allure.step(f"Upload file '{self._file_path}' to '{self._selector}'"):
            actor.ability.page.set_input_files(self._selector, self._file_path)
```

> **Regla:** Cada Interaction hace exactamente UNA operación de Playwright.

---

## Paso 3: Crear el Task

Los Tasks representan acciones de negocio de alto nivel. Componen múltiples Interactions.

**Archivo:** `screenplay/tasks/pay_bill.py`

```python
import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from screenplay.interactions.fill_field import FillField
from screenplay.interactions.click_element import ClickElement


class PayBill:
    """Task to pay a bill on ParaBank."""

    PAYEE_NAME = "input[name='payee.name']"
    PAYEE_ADDRESS = "input[name='payee.address.street']"
    PAYEE_CITY = "input[name='payee.address.city']"
    PAYEE_STATE = "input[name='payee.address.state']"
    PAYEE_ZIP = "input[name='payee.address.zipCode']"
    PAYEE_PHONE = "input[name='payee.phoneNumber']"
    PAYEE_ACCOUNT = "input[name='payee.accountNumber']"
    VERIFY_ACCOUNT = "input[name='verifyAccount']"
    AMOUNT_INPUT = "input[name='amount']"
    SEND_PAYMENT_BUTTON = "input[value='Send Payment']"
    SUCCESS_MESSAGE = "text=Bill Payment Complete"

    def __init__(self, payee_data: dict, amount: str):
        self._payee_data = payee_data
        self._amount = amount

    def perform_as(self, actor) -> None:
        with allure.step(f"Pay bill of ${self._amount} to {self._payee_data.get('name', 'payee')}"):
            actor.attempts_to(
                FillField(self.PAYEE_NAME, self._payee_data["name"]),
                FillField(self.PAYEE_ADDRESS, self._payee_data["address"]),
                FillField(self.PAYEE_CITY, self._payee_data["city"]),
                FillField(self.PAYEE_STATE, self._payee_data["state"]),
                FillField(self.PAYEE_ZIP, self._payee_data["zip_code"]),
                FillField(self.PAYEE_PHONE, self._payee_data["phone"]),
                FillField(self.PAYEE_ACCOUNT, self._payee_data["account_number"]),
                FillField(self.VERIFY_ACCOUNT, self._payee_data["account_number"]),
                FillField(self.AMOUNT_INPUT, self._amount),
                ClickElement(self.SEND_PAYMENT_BUTTON),
            )
            try:
                actor.ability.page.wait_for_selector(
                    self.SUCCESS_MESSAGE, timeout=10000
                )
            except PlaywrightTimeoutError:
                raise TimeoutError(
                    f"Bill payment confirmation not received within 10s. "
                    f"URL: '{actor.ability.page.url}'"
                )
```

> **Reglas del Task:**
> - Usa `with allure.step(f"...")` para que aparezca limpio en Allure
> - Compone Interactions via `actor.attempts_to(...)`
> - Maneja timeouts con mensajes descriptivos

---

## Paso 4: Crear las Questions

Las Questions verifican el estado del sistema después de ejecutar una acción.

**Archivo:** `screenplay/questions/is_bill_payment_successful.py`

```python
import allure


class IsBillPaymentSuccessful:
    """Question: Did the bill payment complete successfully?"""

    def answered_by(self, actor) -> bool:
        with allure.step("Check if bill payment was successful"):
            return actor.ability.page.is_visible("text=Bill Payment Complete")
```

> **Reglas de las Questions:**
> - Usa `with allure.step(...)` (NO `@allure.step` como decorador)
> - Retorna un valor (bool, str, list, etc.)
> - No modifica el estado de la página

---

## Paso 5: Crear los Step Definitions

Los Steps conectan los pasos Gherkin con el Actor y las Tasks/Questions.

**Archivo:** `steps/pago_facturas_steps.py`

```python
"""Step definitions for bill payment feature."""

import allure
from pytest_bdd import when, then, parsers

from screenplay.actors.actor import Actor
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.tasks.pay_bill import PayBill
from screenplay.questions.is_bill_payment_successful import IsBillPaymentSuccessful


# Estado compartido entre steps
_bill_state: dict = {}


@allure.feature("Pago de Facturas")
@when(parsers.parse('el usuario navega a la opción "{option}"'))
def navigate_to_bill_pay(actor: Actor, option: str):
    """Navigate to the Bill Pay page."""
    actor.attempts_to(NavigateTo("billpay.htm"))


@when("completa los datos del beneficiario")
def fill_payee_data(actor: Actor):
    """Fill payee information with test data."""
    _bill_state["payee_data"] = {
        "name": "Test Payee",
        "address": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701",
        "phone": "5551234567",
        "account_number": "12345",
    }


@when(parsers.parse('ingresa el monto de la factura "{amount}"'))
def enter_bill_amount(actor: Actor, amount: str):
    """Store the bill amount."""
    _bill_state["amount"] = amount


@when("confirma el pago")
def confirm_payment(actor: Actor):
    """Execute the bill payment task."""
    actor.attempts_to(
        PayBill(_bill_state["payee_data"], _bill_state["amount"])
    )


@then("el sistema muestra el mensaje de pago exitoso")
def verify_payment_success(actor: Actor):
    """Verify bill payment was successful."""
    assert actor.asks_about(IsBillPaymentSuccessful()), (
        "Expected bill payment success message was not displayed."
    )
```

> **Reglas de los Step Definitions:**
> - Reciben `actor: Actor` como fixture (NO page objects)
> - Usan `actor.attempts_to(Task)` para acciones
> - Usan `actor.asks_about(Question)` para verificaciones
> - Preservan el texto Gherkin en español EXACTO
> - Agregan `@allure.feature("...")` para categorización

---

## Paso 6: Crear el Test Runner y Enlazarlo al Proyecto

El **test runner** es el archivo que conecta todo: enlaza el feature file con los step definitions para que pytest-bdd sepa cómo ejecutar los escenarios.

**Archivo:** `tests/test_pago_facturas.py`

```python
"""Test module for bill payment scenarios."""
from pytest_bdd import scenarios

# Import step definitions so pytest-bdd can discover them
from steps.login_steps import *  # noqa: F401, F403
from steps.pago_facturas_steps import *  # noqa: F401, F403

# Load all scenarios from the feature file
scenarios("pago_facturas.feature")
```

### ¿Cómo se enlaza el feature con el proyecto?

El enlace entre archivos funciona así:

```
pytest.ini                          ← Define dónde buscar features y tests
  ├── testpaths = tests/            ← pytest busca archivos test_*.py aquí
  └── bdd_features_base_dir = features/  ← ruta base para los .feature

tests/test_pago_facturas.py         ← Test Runner
  ├── scenarios("pago_facturas.feature")  ← Enlaza al feature file
  │     └── pytest-bdd busca en: features/pago_facturas.feature
  ├── from steps.login_steps import *     ← Steps compartidos (Background)
  └── from steps.pago_facturas_steps import *  ← Steps específicos

steps/pago_facturas_steps.py        ← Step Definitions
  ├── @when("texto del paso")       ← Debe coincidir EXACTO con el .feature
  └── actor.attempts_to(Task)       ← Delega al Screenplay Pattern

conftest.py                         ← Fixtures automáticas
  ├── actor fixture                 ← Se inyecta en steps que piden "actor"
  ├── page fixture                  ← Página Playwright aislada por test
  └── browser fixture               ← Chromium session-scoped
```

### Diagrama de enlace completo

```
┌─────────────────────────────────────────────────────────────────┐
│ pytest.ini                                                       │
│   testpaths = tests/                                            │
│   bdd_features_base_dir = features/                             │
└──────┬──────────────────────────────┬───────────────────────────┘
       │                              │
       ▼                              ▼
┌──────────────────────┐    ┌──────────────────────────┐
│ tests/               │    │ features/                 │
│  test_pago_facturas.py│    │  pago_facturas.feature   │
│                      │    │                          │
│  scenarios(          │───▶│  # language: es          │
│   "pago_facturas     │    │  Característica: ...     │
│    .feature")        │    │  Escenario: ...          │
└──────────┬───────────┘    └──────────────────────────┘
           │ imports
           ▼
┌──────────────────────┐    ┌──────────────────────────┐
│ steps/               │    │ conftest.py               │
│  pago_facturas_      │◀───│  @pytest.fixture          │
│    steps.py          │    │  def actor(page):         │
│                      │    │    return Actor(           │
│  def confirm(actor): │    │      BrowseTheWeb(page))  │
│    actor.attempts_to │    └──────────────────────────┘
│      (PayBill(...))  │
└──────────────────────┘
```

### Reglas del enlace

| Regla | Detalle |
|---|---|
| Nombre del feature file | Debe coincidir con el string en `scenarios("nombre.feature")` |
| Ruta del feature | Es relativa a `bdd_features_base_dir` definido en `pytest.ini` |
| Steps importados | Se importan con `*` para que pytest-bdd los descubra automáticamente |
| Steps compartidos | Si tu escenario usa los Antecedentes de login, importa `login_steps` |
| Fixture `actor` | Se inyecta automáticamente desde `conftest.py` — no necesitas importarla |
| Texto del step | Debe ser IDÉNTICO entre el `.feature` y el decorador `@when("...")` |

> **Importante:** Si no importas los step definitions en el test runner, pytest-bdd no los encontrará y obtendrás un error `StepDefNotFound`.

---

## Paso 7: Ejecutar y Validar

```bash
# Verificar que pytest descubre los tests
pytest tests/test_pago_facturas.py --collect-only

# Ejecutar el nuevo test
pytest tests/test_pago_facturas.py -v --headed

# Ejecutar con reporte Allure
pytest tests/test_pago_facturas.py -v --alluredir=allure-results

# Ver el reporte
allure serve allure-results
```

---

## Checklist de Archivos Creados

| # | Archivo | Ubicación |
|---|---|---|
| 1 | Feature file | `features/pago_facturas.feature` |
| 2 | Task | `screenplay/tasks/pay_bill.py` |
| 3 | Question | `screenplay/questions/is_bill_payment_successful.py` |
| 4 | Step definitions | `steps/pago_facturas_steps.py` |
| 5 | Test runner | `tests/test_pago_facturas.py` |

---

## Convenciones del Proyecto

| Concepto | Convención |
|---|---|
| Feature files | Español, snake_case: `pago_facturas.feature` |
| Tasks | PascalCase: `PayBill` |
| Interactions | PascalCase: `FillField`, `ClickElement` |
| Questions | PascalCase con prefijo Is/Get: `IsBillPaymentSuccessful` |
| Step definitions | snake_case: `pago_facturas_steps.py` |
| Test runners | snake_case con prefijo test_: `test_pago_facturas.py` |
| Allure steps | `with allure.step(f"...")` (context manager, NO decorador) |
| Selectores CSS | Constantes de clase en MAYÚSCULAS: `SUBMIT_BUTTON = "..."` |

---

## Diagrama de Flujo

```
┌──────────────────────────┐
│ 1. Feature File (.feature)│
│   Gherkin en español      │
└────────────┬─────────────┘
             │ mapea a
             ▼
┌──────────────────────────┐
│ 2. Step Definitions       │
│   actor.attempts_to(Task) │
│   actor.asks_about(Q)     │
└────────────┬─────────────┘
             │ delega a
             ▼
┌──────────────────────────┐
│ 3. Tasks                  │
│   Compone Interactions    │
│   with allure.step(...)   │
└────────────┬─────────────┘
             │ ejecuta
             ▼
┌──────────────────────────┐
│ 4. Interactions           │
│   UNA operación Playwright│
│   with allure.step(...)   │
└──────────────────────────┘
```

---

## Errores Comunes

| Error | Causa | Solución |
|---|---|---|
| `StepDefNotFound` | Step text no coincide exactamente | Verificar que el texto en el step definition sea idéntico al del feature file |
| `fixture 'actor' not found` | Falta importar conftest | El `conftest.py` en la raíz se auto-descubre, verificar que existe |
| `KeyError` en allure.step | Usar `@allure.step("{attr}")` con atributos de instancia | Cambiar a `with allure.step(f"...")` |
| `TimeoutError` | El elemento no aparece a tiempo | Verificar selectores CSS contra la app real |
| `ModuleNotFoundError` | Falta `__init__.py` en subdirectorio | Agregar archivo `__init__.py` vacío |

---

## Recursos

- [ParaBank](https://parabank.parasoft.com/) — Aplicación bajo prueba
- [Playwright Python Docs](https://playwright.dev/python/) — Documentación de Playwright
- [pytest-bdd Docs](https://pytest-bdd.readthedocs.io/) — Documentación de pytest-bdd
- [Allure Report](https://allurereport.org/) — Documentación de Allure
