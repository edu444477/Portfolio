# Despliegue

Arquitectura: frontend estático en Vercel, APIs en Render, PostgreSQL en Neon, Redis en Upstash. Un solo repositorio GitHub, un `git push` despliega todo.

## Servicios

| Componente | Plataforma | URL | Plan |
|---|---|---|---|
| Frontend | Vercel | `https://portfolio-edu444477.vercel.app` | Free |
| API Flask (TFG) | Render | `https://la-nueva-era-api.onrender.com` | Free (750h/mes) |
| PostgreSQL | Neon | pooled: `ep-*.eu-central-1.aws.neon.tech` | Free (3GB) |
| Redis | Upstash | `*.upstash.io:6379` | Free (10K req/día) |

## Repositorio

Un solo repo: `edu444477/Portfolio`.

```
Portfolio/
├── portfolio-frontend/    → Vercel  (Root Directory: portfolio-frontend)
├── la_nueva_era/          → Render  (Root Directory: la_nueva_era)
├── render.yaml            → Blueprint declarativo de Render
└── opencode.json          → Config MCP
```

## Configuración por servicio

### Vercel

| Campo | Valor |
|---|---|
| Root Directory | `portfolio-frontend` |
| Framework Preset | Astro |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Node Version | 20 o superior |

Variables de entorno:

| Key | Valor |
|---|---|
| `PUBLIC_API_URL` | `https://la-nueva-era-api.onrender.com` |

### Render

| Campo | Valor |
|---|---|
| Root Directory | `la_nueva_era` |
| Runtime | Python 3.11.0 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 "app:create_app()"` |
| Health Check Path | `/api/health` |

Variables de entorno (Render → Environment):

| Key | Valor |
|---|---|
| `DATABASE_URL` | pooled connection de Neon **+** `&options=-csearch_path%3Dtfg` |
| `REDIS_URL` | `redis://default:TOKEN@ENDPOINT.upstash.io:6379` |
| `JWT_SECRET_KEY` | `openssl rand -hex 32` |
| `SECRET_KEY` | `openssl rand -hex 32` (distinto) |
| `FLASK_ENV` | `production` |
| `CORS_ORIGINS` | `https://portfolio-edu444477.vercel.app` |
| `PYTHON_VERSION` | `3.11.0` |

### Neon (PostgreSQL)

Schemas creados, uno por proyecto:

```sql
CREATE SCHEMA IF NOT EXISTS tfg;
CREATE SCHEMA IF NOT EXISTS node_api;
CREATE SCHEMA IF NOT EXISTS portfolio;
```

Conexión (Neon Console → Connection Details → **Pooled connection**):

```
postgresql://USER:PASS@ep-XXX-pooler.c-7.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

Añade `&options=-csearch_path%3Dtfg` para que la API del TFG use su schema.

**Pooled** para web services (serverless). **Direct** solo para migraciones Alembic.

### Upstash (Redis)

Redis URL (para `redis-py`):

```
redis://default:TOKEN@ENDPOINT.upstash.io:6379
```

REST URL (para APIs HTTP): `https://ENDPOINT.upstash.io`

## Desplegar

```bash
git add .
git commit -m "descripcion"
git push origin main
```

Vercel y Render hacen deploy automático. No hay pasos manuales.

## Verificar

```bash
# Frontend
curl -I https://portfolio-edu444477.vercel.app

# API
curl https://la-nueva-era-api.onrender.com/api/health

# Schema activo (desde Neon SQL Editor)
SELECT current_schema();
```

## Cold starts

Render duerme el servicio tras 15 min sin tráfico. El primer request tras el sleep tarda ~30s. Es el comportamiento normal del plan free.

Para evitarlo en demos, llama `/api/health` cada 10 minutos desde un cron externo (cron-job.org, GitHub Actions scheduled).

## Troubleshooting

| Síntoma | Causa | Solución |
|---|---|---|
| `astro: command not found` (Vercel) | Root Directory mal | Settings → Root Directory = `portfolio-frontend` |
| `no such table` (API) | falta `search_path` | añade `&options=-csearch_path%3Dtfg` a `DATABASE_URL` |
| CORS error | dominio no está en `CORS_ORIGINS` | añade el dominio exacto, sin barra final |
| Render no clona el repo | GitHub App sin permiso | Settings → Repository → reconnect |
| Build falla en Vercel | schema Zod vs MDX inconsistentes | revisa `src/content/config.ts` contra todos los `.mdx` |

## Coste

Todo en free tier permanente. $0/mes. Sin tarjetas. Límites: Render 750h/mes por servicio, Neon 3GB, Upstash 10K comandos/día, Vercel y Netlify sin límite práctico de despliegue estático.
