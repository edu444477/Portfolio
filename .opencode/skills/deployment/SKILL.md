---
name: deployment
description: Úsala siempre que toques despliegue, variables de entorno, dominios, Vercel, Render, Neon o Upstash. Contiene la arquitectura de hosting, las URLs exactas y los errores conocidos de esta infraestructura.
---

# Despliegue: Vercel + Render + Neon + Upstash

## Arquitectura

```
Vercel     → portfolio-frontend/   (static, dominios gratis, CDN global)
Render     → la_nueva_era/         (web service Flask, 750h/mes gratis)
Neon       → PostgreSQL            (schemas: tfg, node_api, portfolio)
Upstash    → Redis                 (caché, JWT blacklist, rate limiting)
```

Cada proyecto usa **su propio schema** de PostgreSQL. No uses prefijos de tabla: los schemas dan aislamiento real (permisos por usuario, `DROP SCHEMA`, migraciones independientes).

## Variables de entorno exactas

### la_nueva_era (Render)

| Variable | Valor |
|---|---|
| `DATABASE_URL` | La pooled connection de Neon **+** `&options=-csearch_path%3Dtfg` |
| `REDIS_URL` | `redis://default:TOKEN@ENDPOINT.upstash.io:6379` |
| `JWT_SECRET_KEY` | `openssl rand -hex 32` (nunca en el repo) |
| `SECRET_KEY` | `openssl rand -hex 32` (distinto del anterior) |
| `FLASK_ENV` | `production` |
| `CORS_ORIGINS` | `https://portfolio-delta-eight-yx2zi6pmny.vercel.app` (comma-separated, sin barra final) |
| `PYTHON_VERSION` | `3.11.0` |

### portfolio-frontend (Vercel)

| Variable | Valor |
|---|---|
| `PUBLIC_API_URL` | `https://la-nueva-era-api.onrender.com` |

Solo variables `PUBLIC_*` llegan al cliente. Cualquier otra es secreta de Vercel y no debe usarse para datos públicos.

## Configuración de los servicios

**Vercel** → Root Directory: `portfolio-frontend`. Framework: Astro. Output: `dist`. Build: `npm run build`.

**Render** → Root Directory: `la_nueva_era`. Runtime: Python 3.11. Build: `pip install -r requirements.txt`. Start: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 "app:create_app()"`. Health Check Path: `/api/health`.

## Errores conocidos y soluciones

| Síntoma | Causa | Solución |
|---|---|---|
| `astro: command not found` (Vercel) | Root Directory mal configurado, o `package.json` no está en la raíz del proyecto | Vercel Settings → Root Directory = `portfolio-frontend` |
| `we don't have access to your repo` (Render) | La GitHub App de Render no tiene permiso sobre el repo | Render → Settings → Repository → reconnect, o concedes acceso en la GitHub App |
| `no such table` (API) | Falta `search_path` en `DATABASE_URL` | Añade `&options=-csearch_path%3Dtfg` |
| `channel_binding` error | Se editó la connection string de Neon | Restaura `channel_binding=require` |
| Cold start lento en Render | Servicio dormido tras 15 min inactivos | Normal. Configura un cron externo que llame `/api/health` cada 10 min |
| CORS error en el navegador | `CORS_ORIGINS` no incluye el dominio exacto | Verifica el dominio real en la consola del navegador; sin barra final, con `https://` |
| `ModuleNotFoundError` (Render) | `requirements.txt` incompleto o root dir mal | Revisa que el archivo esté en el root dir y que los imports coincidan |

## Reglas

- **Nunca** hardcodees claves, tokens ni URLs con credenciales. Solo variables de entorno y `.env.example` con placeholders.
- **Nunca** subas `.env` al repo. Confirma que está en `.gitignore` antes de commitear.
- **Antes de tocar infraestructura**, confirma con el usuario: cambiar un dominio, añadir un servicio o modificar una variable existente puede romper el deploy en curso.

## Verificación

1. Frontend: Vercel build logs en verde + `curl -I https://portfolio-delta-eight-yx2zi6pmny.vercel.app` devuelve 200.
2. API: `curl https://la-nueva-era-api.onrender.com/api/health` devuelve `{"status":"ok"}`.
3. DB: desde Neon SQL Editor, `SELECT current_schema();` debe devolver el schema del proyecto.
4. Integración: el frontend carga datos de la API sin errores CORS en la consola del navegador.