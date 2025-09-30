Mensajería Cliente-Servidor

Actividad elaborada por:
villalpando Casillas Luz Andrea

Objetivo del programa

Este proyecto corresponde al primer entregable de la materia de Tópicos para el Despliegue de Aplicaciones.
El propósito es diseñar un protocolo propio de comunicación inspirado en los ya existentes (HTTP, TCP/IP, UDP, etc.), con el cual varios clientes puedan intercambiar mensajes en tiempo real a través de un servidor central.

Para ello se emplearán sockets y se desarrollará un sistema de mensajería instantánea entre usuarios conectados a la misma red.

Diseño del protocolo de comunicación

El protocolo se definió de manera sencilla y legible, basado en el intercambio de cadenas de texto con un formato específico. Esto facilita su implementación y guarda relación con otras materias donde se usan patrones similares.

Estructura general de los comandos:

COMANDO|PARAM1|PARAM2|...


Separador: Se usa el carácter | (pipe) para dividir los parámetros.

Codificación: UTF-8, para soportar caracteres especiales (ñ, acentos, símbolos).

Transporte: TCP, por su fiabilidad en la transmisión de datos.

Comandos principales (Cliente → Servidor)

CONNECT – Registrar usuario

CONNECT|nombre_usuario


Propósito: establecer la conexión inicial y registrar un nombre único.

Flujo: cliente envía → servidor valida → respuesta SUCCESS o ERROR.

MESSAGE – Enviar mensaje privado

MESSAGE|destinatario|contenido


Propósito: mandar texto a un usuario específico.

BROADCAST – Enviar mensaje general

BROADCAST|contenido


Propósito: enviar texto a todos los clientes conectados.

GET_USERS – Obtener lista de usuarios

GET_USERS|


Propósito: solicitar la lista actual de participantes.

GET_HISTORY – Solicitar historial

GET_HISTORY|


Propósito: recuperar los mensajes previos del chat general.

PING – Verificar conexión

PING


Propósito: comprobar que la comunicación sigue activa.

Respuesta esperada: PONG.

Respuestas del servidor (Servidor → Cliente)

Confirmaciones

SUCCESS|mensaje → operación correcta.

ERROR|detalle → fallo en la petición.

Mensajes de datos

USER_LIST|usuario1,usuario2,... → lista completa de usuarios.

USER_UPDATE|usuario1,usuario2,... → actualización automática de usuarios conectados.

PRIVATE_MSG|remitente|mensaje → mensaje privado recibido.

BROADCAST_MSG|remitente|mensaje → mensaje general recibido.

HISTORY_MSG|remitente|mensaje → mensaje histórico.

HISTORY_END| → fin del historial.

Notificaciones del sistema

USER_JOINED|usuario → indica que alguien entró.

USER_LEFT|usuario → indica que alguien salió.
