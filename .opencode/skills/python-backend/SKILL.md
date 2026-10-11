---
name: python-backend
description: Úsala siempre que escribas o modifiques código Python del backend Flask en la_nueva_era/ - endpoints, modelos, JWT, migraciones Alembic o conexión a Neon PostgreSQL. Contiene los patrones y trampas de este proyecto.
---

# Backend Flask en la_nueva_era/

## Reglas de oro

- **App factory**: `create_app(config_class=Config)` en `app.py`. Los tests crean la app con una config distinta.
- **Extensiones**: siempre vía `extensions.py` (`db`, `migrate`, `bcrypt`, `jwt`) e `init_extensions(app)`. No instancies extensiones fuera de ahí.
- **Endpoints**: clases Resource en `resources/`, registradas en `register_api_resources(app)`. Flask-RESTful, no Blueprints para la API.
- **Modelos**: SQLAlchemy 2.0 en `models/`, exportados en `models/__init__.py`. Usa `db.Model` y type hints.
- **Auth**: `@jwt_required()` de Flask-JWT-Extended. El token va en `Authorization: Bearer <token>`, no en cookies.

## Conexión a Neon (PostgreSQL) - TRAMPAS

- **`DATABASE_URL` siempre lleva `options=-csearch_path%3Dtfg`**. Sin eso, las tablas se crean en `public` y las queries no las encuentran.
- **Pooled vs direct**: web services usan la pooled connection (hostname con `-pooler`). Migraciones y scripts usan la direct connection. No las mezcles.
- **`channel_binding=require`** no se quita: Neon lo exige para evitar conexiones interceptadas.
- **Servidor**: si `alembic/env.py` necesita `sqlalchemy.url`, léelo de `os.environ['DATABASE_URL']`, nunca hardcodees la URL.
- **Tests**: usa SQLite en memoria o un schema de test. Nunca apuntes los tests a la DB de producción.

## Migraciones (Alembic / Flask-Migrate)

```bash
cd la_nueva_era
flask db migrate -m "descripción del cambio"   # genera la migración
flask db upgrade                                # aplica
```

- **Siempre revisa el archivo generado** antes de aplicar. Alembic a veces genera operaciones destructivas.
- **Una migración = un cambio lógico.** No mezcles refactors con cambios de esquema.
- Nombres de tabla en `snake_case` y en plural (`productos`, `pedidos`).

## Healthcheck (Render lo necesita)

```python
class HealthResource(Resource):
    def get(self):
        return {"status": "ok"}, 200

# en register_api_resources:
api.add_resource(HealthResource, '/api/health')
```

Debe devolver 200 sin tocar la DB (para que un fallo de DB no Tumbe el healthcheck) o con un `SELECT 1` ligero.

## Checklist de revisión

- [ ] ¿El endpoint nuevo está registrado en `register_api_resources`?
- [ ] ¿El endpoint que modifica datos usa `@jwt_required()`?
- [ ] ¿El modelo está importado en `models/__init__.py`?
- [ ] ¿`DATABASE_URL` conserva `search_path`?
- [ ] ¿La migración generada no hace `DROP TABLE` sin querer?
- [ ] ¿Los errores devuelven JSON con mensajes en español?
- [ ] ¿`pytest` pasa?

## Al terminar

Indica qué puntos del checklist has comprobado y cómo.