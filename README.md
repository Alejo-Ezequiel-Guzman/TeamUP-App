# TeamUP - Red Social Deportiva

<div align="center">

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Flet](https://img.shields.io/badge/flet-latest-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**Entrena con tu comunidad, comparte logros y descubre nuevos lugares deportivos**

[Descargar](https://github.com/Alejo-Ezequiel-Guzman/TeamUP-App/releases) • [Documentación](#tabla-de-contenidos) • [Reportar Bug](https://github.com/Alejo-Ezequiel-Guzman/TeamUP-App/issues) • [Solicitar Feature](https://github.com/Alejo-Ezequiel-Guzman/TeamUP-App/issues)

</div>

---

## Tabla de Contenidos

- [Sobre el Proyecto](#sobre-el-proyecto)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Roadmap](#roadmap)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

---

## Sobre el Proyecto

TeamUP es una red social deportiva diseñada para conectar personas apasionadas por el fitness y el deporte. La aplicación permite a los usuarios compartir sus entrenamientos, descubrir lugares deportivos en su ciudad, interactuar con otros atletas y mantenerse motivados en su journey fitness.

### ¿Por qué TeamUP?

- **Comunidad Activa**: Conecta con personas que comparten tus mismos objetivos
- **Descubre Lugares**: Encuentra gimnasios, parques y lugares deportivos cerca de ti
- **Seguimiento**: Registra tus entrenamientos y comparte tu progreso
- **Motivación**: Inspírate con los logros de otros y celebra los tuyos

---

## Características

### Funcionalidades Principales

#### Sistema de Autenticación
- Registro de usuarios con validación
- Login seguro con hash de contraseñas (SHA-256)
- Gestión de sesiones

#### Feed de Entrenamientos
- Publicaciones con imágenes
- Sistema de likes
- Comentarios y conversaciones

#### Perfil de Usuario
- Foto de perfil personalizable
- Biografía y deporte favorito
- Contador de seguidores y seguidos
- Galería de publicaciones

#### Mapa de Entrenamiento
- Lugares deportivos en Buenos Aires
- Filtrado por categorías (clubes, gimnasios, parques, etc.)
- Búsqueda por nombre o deporte
- Integración con Google Maps para direcciones
- Información detallada de cada lugar

#### Sistema de Notificaciones
- Notificaciones de likes
- Notificaciones de comentarios
- Notificaciones de nuevos seguidores
- Marcado de leídas/no leídas
- Gestión individual de notificaciones

#### Temas
- Modo claro y oscuro
- Cambio instantáneo
- Persistencia de preferencias

### Características Técnicas

- Base de datos SQLite local
- Optimización automática de imágenes
- Aplicación portable (no requiere instalación)
- Actualización en tiempo real de la UI
- Interfaz responsive simulando móvil

---

## Instalación

### Para Usuarios Finales

#### Windows

1. Ve a la [página de releases](https://github.com/Alejo-Ezequiel-Guzman/TeamUP-App/releases)
2. Descarga el archivo `TeamUP.exe`
3. Ejecuta el archivo descargado
4. Si Windows Defender muestra una advertencia:
   - Haz clic en "Más información"
   - Luego en "Ejecutar de todas formas"
5. La aplicación se abrirá automáticamente

**Nota**: El ejecutable es completamente portable. No requiere instalación y puedes ejecutarlo desde cualquier ubicación.

### Para Desarrolladores

#### Requisitos Previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Git

#### Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/Alejo-Ezequiel-Guzman/TeamUP-App.git
cd TeamUP-App

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

#### Compilar Ejecutable

```bash
# Instalar PyInstaller
pip install pyinstaller

# Ejecutar script de build
.\build.bat

# El ejecutable estará en dist/TeamUP.exe
```

---

## Uso

### Primer Uso

1. **Registro**: Al abrir la app por primera vez, serás dirigido a la pantalla de registro
2. **Completa tu perfil**: Ingresa tu nombre, email, contraseña y deporte favorito
3. **Explora**: Una vez registrado, podrás explorar el feed, editar tu perfil y descubrir lugares

### Funcionalidades Principales

#### Crear una Publicación
1. Haz clic en el botón "+" en la barra inferior
2. Selecciona una imagen de tu computadora
3. Escribe un caption describiendo tu entrenamiento
4. Haz clic en "Publicar"

#### Interactuar con Publicaciones
- **Like**: Haz clic en el ícono de corazón
- **Comentar**: Haz clic en el ícono de comentario y escribe tu mensaje
- **Ver perfil**: Haz clic en el nombre de usuario

#### Explorar el Mapa
1. Ve a la sección de "Mapa" desde el menú
2. Usa los filtros para encontrar lugares específicos
3. Haz clic en "Ver detalles" para más información
4. Usa "Cómo llegar" para abrir Google Maps con direcciones

#### Gestionar Notificaciones
1. Haz clic en el ícono de campana en la barra superior
2. Revisa tus notificaciones
3. Haz clic en una notificación para ver el contenido relacionado
4. Marca como leída o elimina notificaciones individualmente

---

## Tecnologías

### Frontend
- **Flet** - Framework de UI basado en Flutter
- **Python 3.13** - Lenguaje de programación

### Backend
- **SQLite3** - Base de datos relacional embebida
- **Custom ORM** - Gestión de modelos y base de datos

### Librerías Principales
- **Pillow (PIL)** - Procesamiento y optimización de imágenes
- **hashlib** - Hashing de contraseñas
- **datetime** - Gestión de fechas y timestamps

### Herramientas de Desarrollo
- **Git** - Control de versiones
- **GitHub** - Hosting y colaboración

---

## Estructura del Proyecto

```
TeamUP-App/
│
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias del proyecto
├── build.bat                    # Script para compilar ejecutable
├── .gitignore                   # Archivos ignorados por Git
│
├── database/                    # Capa de datos
│   ├── __init__.py
│   ├── init_db.py              # Inicialización de la base de datos
│   ├── database_manager.py     # Gestión de operaciones CRUD
│   ├── models.py               # Modelos de datos (User, Post, etc.)
│   └── map_data.py             # Datos del mapa de entrenamiento
│
├── pages/                       # Vistas de la aplicación
│   ├── __init__.py
│   ├── home_page.py            # Feed principal
│   ├── profile_page.py         # Perfil de usuario
│   ├── edit_profile_page.py    # Edición de perfil
│   ├── settings_page.py        # Configuración
│   ├── map_page.py             # Mapa de lugares
│   ├── login_page.py           # Inicio de sesión
│   ├── registration_page.py    # Registro de usuarios
│   ├── upload_page.py          # Crear publicaciones
│   └── notifications_page.py   # Notificaciones
│
├── components/                  # Componentes reutilizables
│   ├── __init__.py
│   └── navigation.py           # Barra de navegación y menú
│
├── utils/                       # Utilidades y helpers
│   ├── __init__.py
│   └── theme_manager.py        # Gestión de temas claro/oscuro
│
├── assets/                      # Recursos estáticos
│   └── images/                 # Imágenes de la aplicación
│       ├── posts/              # Publicaciones de usuarios
│       └── profiles/           # Fotos de perfil
│
└── docs/                        # Documentación
    ├── README.md               # Documentación principal
    ├── API.md                  # Documentación de la API interna
    ├── DATABASE.md             # Esquema de base de datos
```

---

## Roadmap

### Versión 1.1 (Próximamente)
- [ ] Sistema de mensajería directa
- [ ] Grupos deportivos
- [ ] Eventos y desafíos
- [ ] Estadísticas personales

### Versión 2.0 (Futuro)
- [ ] Integración con wearables (Fitbit, Apple Watch)
- [ ] Integración real con Google Maps API
- [ ] Sistema de logros y badges
- [ ] App móvil nativa (iOS y Android)
- [ ] Versión web
---

## Contribuir

Las contribuciones son bienvenidas. Si quieres mejorar TeamUP:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b nombre de tu rama`)
3. Commit tus cambios (`git commit -m 'Agrega tus cambios'`)
4. Push a la rama (`git push origin nombre de tu rama`)
5. Abre un Pull Request

### Guías de Contribución

- Lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles
- Sigue las convenciones de código del proyecto
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### Code of Conduct

Este proyecto sigue el Contributor Covenant Code of Conduct. Al participar, se espera que respetes este código.

---

## Reportar Bugs

Si encuentras un bug:

1. Verifica que no esté ya reportado en [Issues](https://github.com/Alejo-Ezequiel-Guzman/TeamUP-App/issues)
2. Abre un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs. actual
   - Screenshots si es posible
   - Tu versión de Windows y TeamUP

---

## Contacto

**Alejo Ezequiel Guzmán**

- GitHub: [@Alejo-Ezequiel-Guzman](https://github.com/Alejo-Ezequiel-Guzman)
- Email: guzman.a.eze@gmail.com

## Apoyo

Si te gusta el proyecto:

- Dale una estrella en GitHub
- Compártelo con tus amigos
- Contribuye con código
- Reporta bugs
- Sugiere nuevas características

---

<div align="center">

**[Volver arriba](#teamup---red-social-deportiva)**

Hecho por Alejo Ezequiel Guzmán

</div>
