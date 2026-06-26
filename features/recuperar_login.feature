# language: es
Característica: Recuperar información de login

  Como usuario registrado que olvidó sus credenciales
  Quiero poder recuperar mi información de login
  Para poder acceder nuevamente a mi cuenta

  Escenario: Recuperar credenciales exitosamente con datos válidos
    Dado el usuario navega a la pagina de recuperacion de login
    Cuando completa el formulario de búsqueda con sus datos personales
    Y hace clic en el botón Find My Login Info
    Entonces el sistema muestra las credenciales recuperadas