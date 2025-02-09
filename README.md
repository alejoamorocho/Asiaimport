# Cosmedical Import

Sistema de gestión de inventario para importaciones de productos cosméticos.

## Estado del Proyecto

### Frontend ⚛️

#### ✅ Completado
- [x] Configuración inicial del proyecto (Vite + React + TypeScript)
- [x] Estructura base del proyecto
- [x] Configuración de Tailwind CSS
- [x] Sistema de autenticación
- [x] Configuración de Redux con slices básicos
- [x] Navbar con menú desplegable accesible
- [x] Páginas base (Products, Categories, Imports)
- [x] Rutas protegidas
- [x] Configuración de ESLint y Prettier
- [x] Gestión completa de productos (CRUD)
- [x] Implementación de componentes reutilizables
- [x] Sistema de validación con Zod
- [x] Búsqueda y filtrado en tablas
- [x] Paginación de resultados
- [x] Formularios de importación
- [x] Integración con sistema de archivos
- [x] Sistema de notificaciones básico
- [x] Sistema de rutas con protección
- [x] Página de login con validación
- [x] Componentes modales y diálogos
- [x] Gestión de estado de autenticación

#### 🔄 En Progreso
- [ ] Sistema de notificaciones en tiempo real
- [ ] Dashboard con estadísticas
- [ ] Sistema de reportes avanzado
- [ ] Filtros avanzados por rango de fechas

#### 📋 Pendiente
- [ ] Exportación de datos a Excel
- [ ] Tests unitarios y de integración
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)

### Backend 🔧

#### ✅ Completado
- [x] Configuración inicial de Django REST Framework
- [x] Configuración de PostgreSQL
- [x] Sistema de autenticación JWT
- [x] Estructura base de modelos
- [x] Configuración del entorno de desarrollo
- [x] Endpoints para gestión de productos
- [x] Sistema de filtros avanzados
- [x] Validaciones de datos básicas
- [x] Permisos básicos (staff/lectura)
- [x] Endpoints para exportación
- [x] Sistema de procesamiento de archivos de importación
- [x] Implementación de Celery para tareas asíncronas
- [x] Sistema de notificaciones por correo
- [x] Gestión de permisos y roles básicos

#### 🔄 En Progreso
- [ ] Sistema de notificaciones en tiempo real
- [ ] Caché y optimización
- [ ] Gestión avanzada de permisos

#### 📋 Pendiente
- [ ] Sistema de logs detallado
- [ ] Tests unitarios y de integración
- [ ] Documentación API (Swagger/OpenAPI)
- [ ] Sistema de backups
- [ ] Rate limiting
- [ ] Seguridad adicional (2FA, etc.)
- [ ] Webhooks para integraciones

### DevOps 🛠️

#### ✅ Completado
- [x] Configuración de Docker
- [x] Docker Compose para desarrollo
- [x] Configuración básica de CI/CD

#### 🔄 En Progreso
- [ ] Mejoras en pipeline de CI/CD
- [ ] Configuración de entornos (dev, staging, prod)
- [x] Monitoreo de aplicación

#### 📋 Pendiente
- [ ] Automatización de backups
- [ ] Configuración de escalado
- [ ] Métricas de rendimiento
- [ ] Logs centralizados
- [ ] Alertas y monitoreo

### Documentación 📚

#### ✅ Completado
- [x] README básico
- [x] Documentación de configuración inicial
- [x] Guía de instalación
- [x] Documentación de endpoints básicos
- [x] Documentación de rutas y autenticación

#### 📋 Pendiente
- [ ] Documentación técnica detallada
- [ ] Guías de usuario
- [ ] Documentación de API completa
- [ ] Guías de contribución
- [ ] Documentación de arquitectura
- [ ] Diagramas de flujo de procesos

## Arquitectura del Backend

El backend está estructurado siguiendo los principios de Clean Architecture y Domain-Driven Design (DDD), con una estricta adherencia a los principios SOLID. Esta arquitectura asegura un código mantenible, testeable y escalable.

### Estructura del Proyecto

```
backend/
└── inventory/
    ├── api/                # Capa de presentación (API REST)
    │   ├── permissions/    # Permisos de la API
    │   ├── urls/          # URLs de la API
    │   ├── views/         # Vistas y ViewSets
    │   └── serializers/   # Serializadores
    ├── application/       # Casos de uso y servicios de aplicación
    │   ├── services/      # Servicios de aplicación
    │   ├── tasks/         # Tareas asíncronas (Celery)
    │   └── dto/           # Objetos de transferencia de datos
    ├── domain/           # Núcleo de la lógica de negocio
    │   ├── models/        # Modelos de dominio (Product, Import, etc.)
    │   │   ├── base.py    # Modelo base abstracto
    │   │   ├── product.py # Entidad de producto
    │   │   └── imports.py # Entidad de importaciones
    │   ├── interfaces/    # Interfaces y contratos
    │   └── validators.py  # Validadores de dominio
    ├── infrastructure/   # Implementaciones técnicas
    │   ├── repositories/  # Implementación de repositorios
    │   └── services/      # Servicios de infraestructura
    └── tests/            # Tests unitarios y de integración
```

### Principios SOLID Implementados

#### 1. Single Responsibility Principle (SRP)
- Cada modelo de dominio (`product.py`, `imports.py`) tiene una única responsabilidad
- Los validadores están separados en `validators.py`
- Separación clara entre la lógica de negocio (domain) y la infraestructura

#### 2. Open/Closed Principle (OCP)
- Modelo base abstracto en `base.py` que permite extensión sin modificación
- Sistema de validadores extensible
- Uso de interfaces para permitir nuevas implementaciones

#### 3. Liskov Substitution Principle (LSP)
- Los modelos heredan de `BaseModel` y mantienen el contrato
- Las implementaciones de repositorio son intercambiables
- Los servicios siguen interfaces bien definidas

#### 4. Interface Segregation Principle (ISP)
- Interfaces pequeñas y específicas en lugar de una grande
- Separación de DTOs por caso de uso
- Permisos granulares en la API

#### 5. Dependency Inversion Principle (DIP)
- La capa de dominio no depende de implementaciones concretas
- Uso de inyección de dependencias en los servicios
- Las capas externas dependen de abstracciones del dominio

### Características Técnicas

#### 1. Validación de Dominio
- Validadores centralizados en `domain/validators.py`
- Reglas de negocio encapsuladas en el dominio
- Validación a nivel de modelo y servicio

#### 2. Gestión de Datos
- Repositorios abstractos para acceso a datos
- DTOs para transferencia segura de información
- Mapeo claro entre modelos de dominio y DTOs

#### 3. API REST
- Endpoints RESTful bien definidos
- Serialización/deserialización consistente
- Sistema de permisos granular

#### 4. Procesamiento Asíncrono
- Tareas en background con Celery
- Procesamiento de importaciones
- Notificaciones asíncronas

### Beneficios de la Arquitectura

1. **Mantenibilidad**
   - Código altamente cohesivo y bajo acoplamiento
   - Fácil identificación y corrección de problemas
   - Cambios localizados sin efectos secundarios

2. **Testabilidad**
   - Tests unitarios por capa
   - Mocking facilitado por interfaces
   - Cobertura completa del dominio

3. **Escalabilidad**
   - Fácil adición de nuevas características
   - Cambios de implementación sin afectar el dominio
   - Preparado para crecimiento futuro

## Arquitectura del Frontend

El frontend está estructurado siguiendo una arquitectura modular basada en características (Feature-based Architecture) y los principios SOLID, utilizando React con TypeScript. Esta arquitectura promueve la reutilización de código, la mantenibilidad y la escalabilidad.

### Estructura del Proyecto

```
frontend/
└── src/
    ├── api/              # Configuración y clientes de API
    ├── components/       # Componentes compartidos
    ├── context/         # Contextos de React
    ├── core/            # Configuraciones core
    ├── features/        # Módulos de características
    │   └── products/    # Ejemplo: Módulo de productos
    │       ├── components/  # Componentes específicos
    │       ├── hooks/      # Hooks personalizados
    │       └── pages/      # Páginas del módulo
    ├── hooks/           # Hooks compartidos
    ├── pages/           # Páginas principales
    ├── routes/          # Configuración de rutas
    ├── services/        # Servicios compartidos
    ├── shared/          # Utilidades compartidas
    ├── store/           # Estado global (Redux)
    ├── styles/          # Estilos globales
    ├── types/           # Tipos TypeScript
    └── utils/           # Utilidades generales
```

### Capas de la Arquitectura

#### 1. Capa de Presentación
- **Propósito**: Maneja la interfaz de usuario
- **Componentes**:
  - `components/`: Componentes UI reutilizables
  - `pages/`: Páginas principales de la aplicación
  - `features/*/components/`: Componentes específicos de características

#### 2. Capa de Lógica de Negocio
- **Propósito**: Maneja la lógica de la aplicación
- **Componentes**:
  - `features/*/hooks/`: Hooks específicos de características
  - `store/`: Estado global y lógica de Redux
  - `services/`: Servicios de negocio

#### 3. Capa de Datos
- **Propósito**: Maneja la comunicación con el backend
- **Componentes**:
  - `api/`: Configuración y clientes de API
  - `services/`: Servicios de datos

### Características Principales

#### 1. Principios SOLID en React
- **Single Responsibility**:
  - Cada componente tiene una única responsabilidad
  - Separación clara entre presentación y lógica
  
- **Open/Closed**:
  - Componentes extensibles mediante props
  - Uso de composición para extender funcionalidad
  
- **Interface Segregation**:
  - Props específicas para cada componente
  - Tipos TypeScript bien definidos
  
- **Dependency Inversion**:
  - Inyección de dependencias via props y contextos
  - Uso de hooks para abstraer lógica

#### 2. Patrones de Diseño
- **Feature Module Pattern**: Organización basada en características
- **Container/Presentational Pattern**: Separación de lógica y UI
- **Custom Hook Pattern**: Abstracción de lógica reutilizable
- **Context Pattern**: Gestión de estado global
- **Render Props Pattern**: Componentes flexibles y reutilizables

#### 3. Características Técnicas
- **TypeScript**: Tipado estático para mejor mantenibilidad
- **Redux Toolkit**: Gestión eficiente del estado global
- **React Query**: Gestión de estado del servidor
- **Zod**: Validación de formularios y datos
- **Tailwind CSS**: Estilos modulares y responsivos

### Beneficios de la Arquitectura

1. **Mantenibilidad**
   - Código organizado por características
   - Componentes pequeños y enfocados
   - Lógica reutilizable en hooks

2. **Escalabilidad**
   - Fácil adición de nuevas características
   - Módulos independientes
   - Patrones consistentes

3. **Rendimiento**
   - Componentes optimizados
   - Carga perezosa de módulos
   - Gestión eficiente del estado

4. **Desarrollo**
   - Estructura clara y predecible
   - Fácil testing
   - Desarrollo en paralelo eficiente

### Ejemplo: Módulo de Productos

El módulo de productos (`features/products/`) demuestra la implementación de estos principios:

```typescript
features/products/
├── components/
│   ├── ProductForm.tsx     # Formulario de producto
│   └── ProductsTable.tsx   # Tabla de productos
├── hooks/
│   ├── useProducts.ts      # Lógica de productos
│   └── useProductForm.ts   # Lógica de formulario
└── pages/
    └── Products.tsx        # Página principal
```

Cada componente sigue el principio de responsabilidad única:
- `ProductForm.tsx`: Maneja la entrada de datos
- `ProductsTable.tsx`: Muestra y gestiona la lista de productos
- `useProducts.ts`: Maneja la lógica de negocio
- `Products.tsx`: Coordina los componentes

## Próximos Pasos Prioritarios

1. Sistema de Notificaciones en Tiempo Real
   - Implementar WebSockets
   - Notificaciones de stock bajo
   - Alertas de importaciones completadas
   - Notificaciones de errores

2. Dashboard y Reportes
   - Implementar dashboard con estadísticas
   - Gráficos de tendencias
   - Reportes personalizables
   - Exportación de datos

3. Testing y Documentación
   - Tests unitarios
   - Tests de integración
   - Documentación API
   - Guías de usuario

## Configuración del Proyecto

### Requisitos Previos

1. Node.js >= 18
2. Python >= 3.10
3. PostgreSQL >= 14
4. Docker y Docker Compose (opcional)

### Configuración Backend

1. Crear entorno virtual:

```shell
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:

```shell
pip install -r requirements.txt
```

3. Configurar variables de entorno:

```shell
cp .env.example .env
```

4. Ejecutar migraciones:

```shell
python manage.py migrate
```

### Configuración Frontend

1. Instalar dependencias:

```shell
cd frontend
npm install
```

2. Configurar variables de entorno:

```shell
cp .env.example .env
```

3. Iniciar servidor de desarrollo:

```shell
npm run dev
```

## Desarrollo

### Convenciones de Código

1. Usar ESLint y Prettier para JavaScript/TypeScript
2. Seguir PEP 8 para Python
3. Documentar funciones y clases principales
4. Usar componentes funcionales y hooks en React
5. Implementar lazy loading para optimización

### Flujo de Trabajo Git

1. Crear rama para nueva característica
2. Desarrollar y probar localmente
3. Crear Pull Request
4. Code Review
5. Merge a main

### Pruebas

1. Frontend: Jest y React Testing Library
2. Backend: Django Test Framework
3. E2E: Cypress

## API

### Endpoints Principales

1. `/api/auth/` - Autenticación
2. `/api/products/` - Gestión de productos
3. `/api/imports/` - Gestión de importaciones
4. `/api/reports/` - Reportes y estadísticas

### Documentación API

La documentación completa de la API está disponible en `/api/docs/`

## Despliegue

### Pasos de Producción

1. Configurar variables de entorno

2. Construir frontend:

```shell
npm run build
```

3. Configurar servidor web:

```nginx
# Configuración de Nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://localhost:3000;
    }
}
```

4. Iniciar servicios:

```shell
python manage.py collectstatic
gunicorn config.wsgi:application
```

### Despliegue con Docker

1. Construir y levantar contenedores:

```shell
docker-compose up -d --build
```

2. Ejecutar migraciones:

```shell
docker-compose exec backend python manage.py migrate
```

## Contribución

1. Fork del repositorio
2. Crear rama de característica
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.

## Soporte

Para soporte, contactar a <support@cosmedical.com>
