# language: es
Característica: Historial de cuenta

Antecedentes:
  Dado el usuario se encuentra en la página de login de ParaBank
  Cuando ingresa el usuario "john" y la contraseña "demo"
  Entonces el sistema muestra el dashboard de la cuenta

Escenario: Visualizar el historial de transacciones de una cuenta
  Cuando el usuario selecciona una cuenta desde el listado
  Entonces el sistema muestra el historial de transacciones
  Y se visualizan los movimientos realizados en la cuenta
