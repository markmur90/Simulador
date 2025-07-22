# Manual de Ayuda - Simulador Bancario

## Índice
1. [Introducción](#introducción)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Funcionalidades Principales](#funcionalidades-principales)
5. [Seguridad y Autenticación](#seguridad-y-autenticación)
6. [Transferencias](#transferencias)
7. [Administración](#administración)
8. [Solución de Problemas](#solución-de-problemas)

## Introducción

Este simulador bancario es un sistema Django que simula operaciones bancarias, especialmente enfocado en transferencias SEPA. El sistema consta de dos proyectos principales:

### API Project
- Backend API que envía solicitudes al servidor
- Maneja la autenticación y autorización
- Procesa las solicitudes de transferencias
- Implementa validaciones de seguridad

### Simulator Project
- Servidor que procesa las solicitudes de la API
- Simula el comportamiento de un banco real
- Maneja estados de transferencias
- Implementa lógica de negocio bancaria

### Características Principales
- Gestión completa de transferencias SEPA
- Sistema de autenticación múltiple (JWT, OTP, PhotoTAN, PushTAN)
- Registro detallado de actividades y logs
- Interfaz de administración personalizada
- Gestión de cuentas deudoras y acreedoras
- Validación de IBAN y datos bancarios
- Monitoreo de transacciones en tiempo real
- Estadísticas y reportes detallados

## Estructura del Proyecto

### Directorios Principales
```
simulador_banco/
├── banco/              # Aplicación principal
│   ├── models.py       # Modelos de datos
│   ├── views.py        # Vistas y lógica
│   ├── urls.py         # URLs y rutas
│   └── admin.py        # Configuración admin
├── services/           # Servicios de negocio
│   ├── transfer_services.py
│   ├── security_services.py
│   ├── creditor_services.py
│   └── statistics_services.py
├── templates/          # Plantillas HTML
│   ├── banco/
│   └── api/
├── static/            # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
└── docs/              # Documentación
```

### Componentes Clave

#### banco/
- **models.py**: Define los modelos de datos
  - Transfer
  - OTPChallenge
  - DebtorAccount
  - CreditorAccount
  - SystemLog
  - UserActivity
  - TransferStatistics

- **views.py**: Implementa la lógica de negocio
  - Procesamiento de transferencias
  - Validación de datos
  - Manejo de autenticación
  - Generación de reportes

- **urls.py**: Define las rutas de la aplicación
  - API endpoints
  - Vistas web
  - Rutas administrativas

#### services/
- **transfer_services.py**
  - Procesamiento de transferencias
  - Validación de fondos
  - Control de estados
  - Logging de operaciones

- **security_services.py**
  - Generación de OTP
  - Validación de tokens
  - Control de acceso
  - Seguridad de datos

- **creditor_services.py**
  - Gestión de acreedores
  - Validación de cuentas
  - Procesamiento de IBAN
  - Actualización de datos

- **statistics_services.py**
  - Generación de estadísticas
  - Monitoreo de actividad
  - Reportes de uso
  - Análisis de datos

#### templates/
- Interfaces de usuario modulares
- Formularios de transferencia
- Pantallas de autenticación
- Vistas de administración

#### static/
- Hojas de estilo CSS
- Scripts JavaScript
- Imágenes y recursos
- Archivos de configuración

## Configuración del Entorno

### Requisitos Previos
- Python 3.x
- Django (versión especificada en requirements.txt)
- Entorno virtual Python
- Base de datos SQLite (configurada)
- Dependencias adicionales:
  - pyotp
  - django-rest-framework
  - pillow (para PhotoTAN)
  - cryptography

### Pasos de Instalación

1. Activar el entorno virtual:
```bash
source ~/envSIM/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la base de datos:
```bash
python manage.py migrate
```

4. Crear superusuario:
```bash
python manage.py createsuperuser
```

5. Configurar variables de entorno:
```bash
export DJANGO_SETTINGS_MODULE=simulador_banco.settings
export SECRET_KEY='tu_clave_secreta'
export DEBUG=True
```

6. Iniciar el servidor:
```bash
python manage.py runserver
```

### Configuración Adicional

#### Base de Datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Seguridad
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Funcionalidades Principales

### 1. Gestión de Cuentas

#### Cuentas Deudoras
- Creación y gestión de cuentas
- Validación de IBAN
- Control de saldo
- Historial de movimientos
- Límites de transferencia
- Monitoreo de actividad

#### Cuentas Acreedoras
- Registro de beneficiarios
- Validación de datos bancarios
- Gestión de direcciones
- Historial de transferencias
- Categorización de cuentas

#### Validación de IBAN
- Verificación de formato
- Validación de país
- Control de dígitos
- Registro de intentos

#### Estado de Cuenta
- Saldo actual
- Movimientos recientes
- Transferencias pendientes
- Historial de operaciones
- Reportes detallados

### 2. Transferencias

#### Tipos
- SEPA Credit Transfer
- Transferencias internas
- Pagos programados
- Transferencias masivas

#### Validación
- Fondos suficientes
- Límites diarios
- Datos del beneficiario
- Formato SEPA

#### Procesamiento
- Verificación de datos
- Generación de OTP
- Confirmación
- Ejecución
- Notificación

#### Seguimiento
- Estado en tiempo real
- Historial detallado
- Notificaciones
- Reportes

### 3. Sistema de Autenticación

#### JWT
- Generación de tokens
- Validación
- Renovación
- Control de sesión

#### OTP
- Generación de códigos
- Validación
- Tiempo de expiración
- Intentos máximos

#### PhotoTAN
- Generación de imágenes
- Escaneo
- Validación
- Seguridad visual

#### PushTAN
- Notificaciones móviles
- Confirmación en app
- Sincronización
- Seguridad adicional

### 4. Monitoreo y Logs

#### Registro de Actividades
- Acciones de usuario
- Transferencias
- Errores
- Seguridad

#### Logs de Transferencias
- Estado
- Timestamps
- Detalles
- Errores

#### Estadísticas
- Volumen de operaciones
- Usuarios activos
- Tipos de transferencia
- Análisis temporal

#### Monitoreo
- Rendimiento
- Seguridad
- Disponibilidad
- Errores

## Seguridad y Autenticación

### JWT (JSON Web Tokens)

#### Configuración
```python
JWT_AUTH = {
    'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}
```

#### Funcionalidades
- Autenticación de API
- Control de sesión
- Renovación automática
- Revocación de tokens

### OTP (One-Time Password)

#### Configuración
```python
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 3
```

#### Características
- Códigos de 6 dígitos
- Expiración configurable
- Control de intentos
- Registro de uso

### PhotoTAN

#### Generación
- Códigos QR únicos
- Datos encriptados
- Tiempo limitado
- Validación visual

#### Verificación
- Escaneo seguro
- Validación en tiempo real
- Control de intentos
- Registro de uso

### PushTAN

#### Notificaciones
- Envío seguro
- Confirmación inmediata
- Datos encriptados
- Control de dispositivos

#### Seguridad
- Autenticación de dispositivo
- Encriptación end-to-end
- Tiempo limitado
- Registro de actividad

## Transferencias

### Tipos de Transferencias

#### 1. Transferencias SEPA
- Validación IBAN
- Límites configurables
- Confirmación multi-factor
- Procesamiento SEPA

#### 2. Transferencias Internas
- Procesamiento inmediato
- Sin OTP requerido
- Validación simplificada
- Confirmación directa

### Estados de Transferencia

#### PDNG (Pending)
- Transferencia creada
- Pendiente de autorización
- OTP no validado
- Fondos no verificados

#### ACCP (Accepted)
- Datos validados
- OTP confirmado
- Pendiente de proceso
- Fondos reservados

#### RJCT (Rejected)
- Datos inválidos
- OTP incorrecto
- Fondos insuficientes
- Error de proceso

#### ACSP (In Process)
- En procesamiento
- Fondos verificados
- OTP validado
- Pendiente de completar

#### ACSC (Completed)
- Transferencia exitosa
- Fondos transferidos
- Proceso completado
- Notificación enviada

### Proceso de Transferencia

#### 1. Creación
- Validación de datos
- Verificación de cuenta
- Generación de ID
- Estado inicial

#### 2. Validación
- Formato de datos
- Existencia de cuentas
- Fondos disponibles
- Límites de transferencia

#### 3. Generación OTP/TAN
- Creación de desafío
- Envío de código
- Tiempo de espera
- Control de intentos

#### 4. Confirmación
- Validación de código
- Verificación de tiempo
- Control de estado
- Registro de confirmación

#### 5. Procesamiento
- Reserva de fondos
- Actualización de saldos
- Registro de movimientos
- Actualización de estado

#### 6. Finalización
- Confirmación final
- Notificaciones
- Actualización de logs
- Generación de comprobante

## Administración

### Panel de Administración

#### Gestión de Usuarios
- Creación de cuentas
- Asignación de roles
- Control de permisos
- Monitoreo de actividad

#### Monitoreo
- Estado del sistema
- Transferencias activas
- Logs en tiempo real
- Alertas y notificaciones

#### Configuración
- Parámetros del sistema
- Límites y restricciones
- Seguridad
- Notificaciones

#### Logs
- Actividad del sistema
- Errores y advertencias
- Auditoría
- Reportes

### Roles de Usuario

#### 1. Superusuario
- Acceso total
- Configuración global
- Gestión de usuarios
- Auditoría completa

#### 2. Administrador
- Gestión de transferencias
- Monitoreo de actividades
- Reportes y estadísticas
- Control de usuarios

#### 3. Usuario Regular
- Transferencias básicas
- Estado de cuenta
- Historial personal
- Configuración básica

### Estadísticas y Reportes

#### Volumen
- Cantidad de transferencias
- Montos totales
- Promedios diarios
- Tendencias

#### Análisis
- Patrones de uso
- Comportamiento usuario
- Tipos de operación
- Errores comunes

#### Seguridad
- Intentos fallidos
- Actividad sospechosa
- Bloqueos de cuenta
- Alertas generadas

#### Rendimiento
- Tiempo de respuesta
- Disponibilidad
- Errores del sistema
- Uso de recursos

## Solución de Problemas

### Problemas Comunes

#### 1. Error de Autenticación
- Verificar credenciales
- Comprobar token JWT
- Validar permisos
- Revisar logs

#### 2. Fallo en Transferencias
- Verificar saldo
- Comprobar límites
- Validar IBAN
- Revisar estado

#### 3. Problemas de OTP
- Tiempo expirado
- Intentos excedidos
- Código inválido
- Error de generación

### Logs y Depuración

#### Ubicación
- /logs/
- debug.log
- error.log
- security.log

#### Niveles
- DEBUG
- INFO
- WARNING
- ERROR

#### Formato
- Timestamp
- Tipo de evento
- Mensaje
- Detalles

### Contacto y Soporte

#### Documentación
- /docs/
- Guías técnicas
- Manuales
- FAQ

#### Ayuda
- ayuda.txt
- Guías paso a paso
- Ejemplos
- Tutoriales

#### Soporte Técnico
- Contacto
- Reportes de error
- Solicitudes de mejora
- Consultas técnicas

## Notas Adicionales

### Mejores Prácticas

#### 1. Entorno
- Activar virtualenv
- Actualizar dependencias
- Revisar logs
- Backup regular

#### 2. Desarrollo
- Seguir estándares
- Documentar cambios
- Pruebas unitarias
- Control de versiones

#### 3. Seguridad
- Actualizar contraseñas
- Monitorear actividad
- Revisar permisos
- Mantener actualizado

#### 4. Mantenimiento
- Limpieza de logs
- Optimización DB
- Backup datos
- Monitoreo rendimiento

### Seguridad

#### 1. Acceso
- Contraseñas seguras
- 2FA activado
- Sesiones limitadas
- Control de IP

#### 2. Datos
- Encriptación
- Backups seguros
- Acceso controlado
- Auditoría regular

#### 3. Monitoreo
- Actividad sospechosa
- Intentos fallidos
- Cambios críticos
- Alertas automáticas

### Mantenimiento

#### 1. Rutinario
- Limpieza logs
- Backup datos
- Actualización sistema
- Verificación seguridad

#### 2. Preventivo
- Monitoreo rendimiento
- Análisis tendencias
- Optimización recursos
- Pruebas periódicas

#### 3. Correctivo
- Solución errores
- Actualización parches
- Mejoras sistema
- Documentación cambios

## Seguridad y Autenticación

### Encriptación de Datos

#### EncryptedCharField
```python
class EncryptedCharField(models.Field):
    """Campo personalizado para cifrado AES256+HMAC"""
    # Configuración
    FIELD_ENCRYPTION_KEYS = [key1, key2, ...]  # Rotación de claves
    # Cifrado automático de datos sensibles
```

#### Validadores
```python
# Validadores de datos bancarios
country_validator = RegexValidator(r'^[A-Z]{2}$')
iban_validator = RegexValidator(r'^[A-Z]{2}[0-9A-Z]{13,32}$')
currency_validator = RegexValidator(r'^[A-Z]{3}$')
```

### Sistema de Logs

#### SystemLog
- Niveles: INFO, WARNING, ERROR, CRITICAL, DEBUG
- Acciones registradas:
  - LOGIN/LOGOUT
  - TRANSFER_CREATE/UPDATE
  - OTP_GENERATE/VALIDATE
  - USER_CREATE/UPDATE
  - ACCOUNT_CREATE/UPDATE
  - API_CALL
  - SECURITY_EVENT

#### Formato de Log
```python
{
    'timestamp': '2024-03-21T10:30:00Z',
    'level': 'INFO',
    'action': 'TRANSFER_CREATE',
    'user': 'username',
    'ip_address': '192.168.1.1',
    'description': 'Detalle de la acción',
    'additional_data': {...}
}
```

### Validación de Transferencias

#### Validaciones Automáticas
1. **Saldo Suficiente**
```python
if debtor_account.balance < amount:
    raise ValidationError('Saldo insuficiente')
```

2. **Límites de Transferencia**
```python
RATE_LIMIT = 5
WINDOW_MINUTES = 5
```

3. **Moneda Compatible**
```python
if cuenta_origen.currency != cuenta_destino.currency:
    raise ValidationError('Monedas incompatibles')
```

4. **Datos Bancarios**
- Formato IBAN
- Código de país
- Código de moneda
- Existencia de cuentas

#### Control de Duplicados
```python
existing = Transfer.objects.filter(payment_id=payment_id).first()
if existing:
    return existing  # Control de idempotencia
```

## API y Endpoints

### Endpoints Principales

#### Autenticación
```
POST /api/login/
POST /api/token
POST /oidc/token
GET  /oidc/authorize
```

#### Transferencias
```
POST /api/send-transfer
POST /api/status-transfer
POST /payments
POST /api/transferencias/entrantes/
```

#### Gestión de Cuentas
```
GET  /api/get-accounts-by-debtor/
GET  /api/get-accounts-by-creditor/
```

### Formatos de Respuesta

#### Éxito
```json
{
    "payment_id": "...",
    "status": "PDNG",
    "challenge_id": "...",
    "otp_required": true
}
```

#### Error
```json
{
    "error": "Descripción del error",
    "status": 400
}
```

## Interfaz de Usuario

### Formularios

#### TransferForm
- Validación en tiempo real
- Actualización dinámica de saldos
- Verificación de límites
- Selección de cuentas filtrada

#### Validación JavaScript
```javascript
function validateForm() {
    // Validación de campos requeridos
    // Validación de montos
    // Validación de cuentas
    // Validación de saldos
}
```

### Componentes Dinámicos

#### Balance Info
```javascript
function updateBalanceInfo() {
    // Muestra saldo disponible
    // Actualiza información de cuenta
    // Valida límites
}
```

## Mantenimiento y Monitoreo

### Monitoreo en Tiempo Real

#### Métricas Clave
- Transferencias por minuto
- Tasa de error
- Tiempo de respuesta
- Uso de recursos

#### Alertas
- Intentos fallidos de autenticación
- Errores de transferencia
- Problemas de conexión
- Límites excedidos

### Backup y Recuperación

#### Estrategia de Backup
1. Backup diario de base de datos
2. Backup semanal completo
3. Retención de 30 días
4. Verificación automática

#### Procedimiento de Recuperación
1. Detener servicios
2. Restaurar backup
3. Verificar integridad
4. Reiniciar servicios

## Integración y APIs

### API Externa

#### Headers Requeridos
```
Authorization: Bearer <token>
Content-Type: application/json
Idempotency-Key: <unique-id>
```

#### Límites de API
- Rate limit: 100 req/min
- Timeout: 30 segundos
- Tamaño máximo: 10MB
- Conexiones máximas: 50

### Webhooks

#### Eventos Disponibles
- transfer.created
- transfer.completed
- transfer.failed
- otp.generated
- otp.validated

#### Formato de Webhook
```json
{
    "event": "transfer.completed",
    "timestamp": "2024-03-21T10:30:00Z",
    "data": {
        "payment_id": "...",
        "status": "ACSC",
        "amount": "100.00",
        "currency": "EUR"
    }
}
```

---

Este manual está en constante actualización. Para más información específica, consultar la documentación técnica en `/docs/` o contactar al equipo de desarrollo.

### Historial de Actualizaciones
- Versión inicial: 1.0
- Última actualización: [Fecha actual]
- Próxima revisión: [3 meses desde fecha actual]
- Cambios recientes:
  - Agregada documentación de API
  - Actualizada sección de seguridad
  - Mejorada documentación de validaciones
  - Agregados ejemplos de código 