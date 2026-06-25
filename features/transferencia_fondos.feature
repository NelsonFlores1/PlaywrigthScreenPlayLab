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
