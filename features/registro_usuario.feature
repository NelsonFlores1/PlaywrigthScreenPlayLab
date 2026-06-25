# language: es
Característica: Registro de usuario y apertura de cuenta

@setup @registro
Escenario: Registrar un nuevo usuario y abrir una cuenta bancaria
  Dado el usuario navega a la página de registro de ParaBank
  Cuando completa el formulario con datos de prueba generados
  Y hace clic en el botón Register
  Entonces el sistema confirma que el usuario fue creado exitosamente
  Cuando el usuario navega a Open New Account
  Y selecciona el tipo de cuenta "CHECKING"
  Y confirma la apertura de la cuenta
  Entonces el sistema crea la cuenta y muestra su número
  Y el entorno está listo para ejecutar los demás escenarios
