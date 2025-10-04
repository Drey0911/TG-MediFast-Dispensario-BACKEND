# MediFast

<p align="center">
  <img src="./static/img/logo-green.png" alt="MediFast Logo" width="300">
</p>

## Descripción del Proyecto

MediFast es una plataforma integral para la gestión de dispensarios de medicamentos, diseñada para optimizar la disponibilidad, distribución y seguimiento de medicamentos. El sistema permite la administración de inventario, notificaciones automáticas y seguimiento de recolecciones, mejorando la experiencia tanto para administradores como para usuarios finales.

## Características Principales

- **Gestión de Medicamentos**: Inventario completo con información detallada de cada medicamento
- **Control de Disponibilidad**: Seguimiento en tiempo real de la disponibilidad de medicamentos
- **Sistema de Recolecciones**: Gestión de solicitudes y programación de recolecciones
- **Notificaciones por WhatsApp**: Alertas automáticas para usuarios sobre disponibilidad y recordatorios
- **Panel de Administración**: Interfaz web para gestión completa del sistema
- **API REST**: Endpoints para integración con aplicaciones móviles y otros sistemas
- **WebSockets**: Comunicación en tiempo real para actualizaciones instantáneas

## Estructura del Proyecto

```
backend/
├── app.py                 # Punto de entrada principal de la aplicación
├── config/                # Configuración de la base de datos y conexiones
├── models/                # Modelos de datos (SQLAlchemy)
├── routes/                # Rutas API y endpoints
├── services/              # Servicios de negocio y lógica de la aplicación
├── static/                # Archivos estáticos (imágenes, CSS, JS)
├── templates/             # Plantillas Jinja2 para el panel de administración
├── socketsExtends.py      # Configuración de WebSockets
└── requirements.txt       # Dependencias del proyecto
```

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL (alojada en Clever Cloud en este caso, pero se podria local siempre y cuando sea MYSQL)
- **Plantillas**: Jinja2 para el panel de administración
- **Autenticación**: JWT (JSON Web Tokens)
- **Comunicación en Tiempo Real**: Flask-SocketIO
- **Tareas Programadas**: APScheduler
- **Notificaciones**: Integración con la API de WhatsApp Business
- **Rutas**: API Rest y sesiones de usuario admin 

## Requisitos

- Python 3.8+
- MySQL (local o montado, ya que las tablas se quedan de manera automatica)
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
   ```
   git clone <url-del-repositorio>
   cd backend
   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno (crear archivo `.env` en la raíz del proyecto):
   ```
   # Configuración de la base de datos
   DB_HOST=<host_mysql>
   DB_USER=<usuario_mysql>
   DB_PASSWORD=<contraseña_mysql>
   DB_NAME=<nombre_base_datos>
   
   # Configuración de JWT
   JWT_SECRET_KEY=<clave_secreta_jwt>
   JWT_ACCESS_TOKEN_EXPIRES=<tiempo_expiracion_en_segundos>
   
   # Configuración de WhatsApp API
   WHATSAPP_API_URL=<url_api_whatsapp>
   WHATSAPP_API_TOKEN=<token_api_whatsapp>
   WHATSAPP_PHONE_ID=<id_telefono_whatsapp>
   
   # Configuración del servidor
   FLASK_DEBUG=True  # Solo en desarrollo
   PORT=8000
   ```

4. Iniciar el servidor en modo desarrollo:
   ```
   python app.py
   ```

## Rutas API

### Rutas de Usuario (`/api/users`)
- `GET /api/users` - Obtener todos los usuarios
- `GET /api/users/<id>` - Obtener usuario por ID
- `POST /api/users` - Crear nuevo usuario
- `PUT /api/users/<id>` - Actualizar usuario
- `DELETE /api/users/<id>` - Eliminar usuario
- `POST /api/users/login` - Autenticación de usuario (genera token JWT)
- `POST /api/users/register` - Registro de nuevo usuario
- `GET /api/me` - Saber quien eres en el sistema actual logeado

### Rutas de Medicamentos (`/api/medicamentos`)
- `GET /api/medicamentos` - Obtener todos los medicamentos
- `GET /api/medicamentos/<id>` - Obtener medicamento por ID
- `POST /api/medicamentos` - Crear nuevo medicamento
- `PUT /api/medicamentos/<id>` - Actualizar medicamento
- `DELETE /api/medicamentos/<id>` - Eliminar medicamento
- `GET /api/medicamentos/search` - Buscar medicamentos por nombre o descripción

### Rutas de Disponibilidad (`/api/disponibilidad`)
- `GET /api/disponibilidad` - Obtener todas las disponibilidades
- `GET /api/disponibilidad/<id>` - Obtener disponibilidad por ID
- `POST /api/disponibilidad` - Crear nueva disponibilidad
- `PUT /api/disponibilidad/<id>` - Actualizar disponibilidad
- `DELETE /api/disponibilidad/<id>` - Eliminar disponibilidad

### Rutas de Recolección (`/api/recolecciones`)
- `GET /api/recolecciones` - Obtener todas las recolecciones
- `GET /api/recolecciones/<id>` - Obtener recolección por ID
- `POST /api/recolecciones` - Crear nueva recolección
- `PUT /api/recolecciones/<id>` - Actualizar recolección
- `DELETE /api/recolecciones/<id>` - Eliminar recolección

### Rutas de Favoritos (`/api/favoritos`)
- `GET /api/favoritos/user/<user_id>` - Obtener favoritos de un usuario
- `POST /api/favoritos` - Añadir medicamento a favoritos
- `DELETE /api/favoritos/<id>` - Eliminar de favoritos

## Panel de Administración

El panel de administración está construido con plantillas Jinja2 y proporciona una interfaz web para gestionar todos los aspectos del sistema.

### Rutas del Panel de Administración
- `/` - Dashboard principal
- `/login` - Inicio de sesión para administradores
- `/medicamentos` - Gestión de medicamentos
- `/medicamentos/add` - Añadir nuevo medicamento
- `/medicamentos/edit/<id>` - Editar medicamento
- `/medicamentos/view/<id>` - Ver detalles de medicamento
- `/disponibilidad` - Gestión de disponibilidad
- `/disponibilidad/add` - Añadir nueva disponibilidad
- `/disponibilidad/edit/<id>` - Editar disponibilidad
- `/recolecciones` - Gestión de recolecciones
- `/recolecciones/edit/<id>` - Editar recolección
- `/sedes` - Gestión de sedes
- `/sedes/add` - Añadir nueva sede
- `/sedes/edit/<id>` - Editar sede
- `/users` - Gestión de usuarios
- `/users/add` - Añadir nuevo usuario
- `/users/edit/<id>` - Editar usuario

## Seguridad

Todas las rutas API requieren autenticación mediante token JWT, excepto las rutas de inicio de sesión. El token debe incluirse en el encabezado de la solicitud como `Authorization: Bearer <token>` si se desea revisar con Postman o otro software es necesario primero logearse con la api/login.

## WebSockets

El sistema utiliza WebSockets para proporcionar actualizaciones en tiempo real sobre:
- Cambios en la disponibilidad de medicamentos
- Nuevas recolecciones
- Actualizaciones de estado de recolecciones
- Actualizaciones en los usuarios o modificaciones en tiempo real
- Tareas y vistas en tiempo real (medicamentos, recolecciones, usuarios, etc...)

## Servicios Programados

El sistema utiliza APScheduler para ejecutar tareas programadas:
- Envío diario de recordatorios para recolecciones pendientes
- Monitoreo de stock de medicamentos
- Notificaciones automáticas de disponibilidad

## Integración con WhatsApp

El sistema se integra con la [API de WhatsApp Business](https://developers.facebook.com/docs/whatsapp/api/overview) para enviar notificaciones automáticas a los usuarios sobre:
- Disponibilidad de medicamentos
- Recordatorios de recolección
- Cambios en el estado de las recolecciones
- Cambio de contraseña

( Se recomienda en produccion usar la API verificada, usando plantillas para la funcionalidad, actualmente, se usa el numero de prueba de WhatsApp
y se debe escribir un mensaje previamente para el envio en la ventana de 24 horas, esto solo en modo desarrollo o prototipo en entorno real, se
necesitaria la API verificada con WhatsApp Business)

## Usuario administrador

Para usarse la aplicacion de forma correcta y pruebas tenemos un usuario predeterminado:

DNI: 10101010
Pass: Admin.123456789

en tu motor de BD sea local o desplegado pega lo siguiente en el apartado de sentencias SQL o de creacion:

INSERT INTO `usuarios` (`id`, `nombre`, `apellidos`, `dni`, `telefono`, `password`, `rol`) VALUES
(1, 'MediFast', 'Dispensario', '10101010', '+573000000000', '$2b$12$8uNWOICxpZPmFb84U.8D9eGiGslHPHUd4aDT9.uvjTs9ZT1tBnvYG', 'admin');


## Licencia

Todos los derechos reservados. © 2025 Andrey Stteven Mantilla Leon y Daniel Esteban Pinzon Cardenas.

Este software es propiedad de sus creadores y no puede ser reproducido, distribuido o utilizado sin autorización expresa.