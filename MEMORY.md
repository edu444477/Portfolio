# MEMORY.md — Portfolio Personal

Memoria del proyecto entre sesiones. Máximo ~50 líneas.

## Estado actual (2026-10-11)

- **Infraestructura definida**: Vercel (frontend static) + Render (APIs) + Neon (PostgreSQL schemas) + Upstash (Redis)
- **Neon**: proyecto `rough-bar-22432276`, schemas `tfg`, `node_api`, `portfolio` creados. Usuario `tfg_user` con password hardcodeada en DB (⚠️ mover a variable de entorno)
- **Upstash**: DB `natural-rattler-221300`, REST URL + token disponibles
- **Render**: Web Service `la-nueva-era-api` creado, deploy desde GitHub (repo `edu444477/Portfolio`)
- **Vercel**: proyecto creado, deploy falló (repo vacío al momento). Root Directory: `portfolio-frontend`
- **TFG (la_nueva_era/)**: Flask 3 + Flask-RESTful + SQLAlchemy + JWT + React 18 (TFG e-commerce). requirements.txt, config.py (Neon+search_path), Dockerfile, entrypoint.sh, alembic.ini, .env.example creados. Falta endpoint `/api/health` para el healthcheck de Render
- **Frontend (portfolio-frontend/)**: base creada (package.json, astro.config.mjs, tailwind.config.mjs, tsconfig.json, vercel.json, .env.example, content/config.ts, content/projects/la_nueva_era.mdx, content/experience/2024_tfg.mdx, content/tech/stack.json, components/ui/*, components/layout/*, components/sections/*). FALTA: pages (index.astro, projects/[slug].astro, api/contact.ts), styles/global.css, lib/utils.ts, lib/constants.ts, .env.local
- **.opencode/ COMPLETO**: 4 agents (coordinator, planner, implementer, reviewer), 10 commands (feature + 9 sdd-*), 5 skills propias (sdd, astro-react-tailwind, python-backend, deployment, accessibility) + README de skills de comunidad
- **Docs**: docs/constitution.md (6 principios), docs/deployment.md (guía completa)
- **Deploy config**: render.yaml (Blueprint), opencode.json (MCP: chrome-devtools + context7)
- **Spec 001**: NO CREADA. Siguiente paso del flujo SDD

## Decisiones (y por qué)

- **Astro + React islands** en vez de React SPA: mejor rendimiento (HTML estático), SEO perfecto, menos JS enviado. React solo donde hay interactividad real.
- **Tailwind CSS** en vez de CSS vanilla: consistencia, rapididad, dark mode trivial con clases.
- **Neon schemas en vez de prefijos de tabla**: aislamiento real (DROP SCHEMA, permisos por user, migraciones independientes) vs prefijos que solo son convención de nombres.
- **Render en vez de Northflank/Fly.io/Railway**: Northflank pide tarjeta para DBs; Fly.io eliminó free tier permanente; Railway tiene trial de $5 y luego $1/mínimo. Render: 750h/mes gratis sin tarjeta.
- **Neon + Upstash en vez de DB gestionada por Render**: Render cobra ($7/mes) su PostgreSQL/Redis tras 90 días. Neon/Upstash tienen free tier permanente.
- **Vercel en vez de Cloudflare Pages**: mejor DX con Astro, preview deployments, analytics gratis.
- **Schemas separados por proyecto**: `tfg`, `node_api`, `portfolio`. Permite isolates tests, deploys independientes, y un solo cluster DB.

## Aprendizajes y errores a evitar

- **Vercel falla con "astro: command not found"** si el Root Directory no es `portfolio-frontend` o si no hay `package.json` ahí. Verificar siempre el root dir en Vercel settings.
- **Render: "we don't have access to your repo"**: la GitHub App de Render necesita acceso explícito al repo. Configurar en Render → Settings → Repository.
- **Neon connection string**: la pooled connection tiene `-pooler` en el hostname y `channel_binding=require` en los params. No quitarlo.
- **Upstash REST vs Redis URL**: `UPSTASH_REDIS_REST_URL` es para HTTP (requests), `REDIS_URL` es para clientes Redis nativos (aioredis, redis-py). Render necesita `REDIS_URL` formato `redis://`.
- **Content Collections**: si el schema Zod requiere un campo y un MDX no lo tiene, `npm run build` falla. Todos los MDX deben cumplir el schema.

## Próximos pasos

- [ ] **Reiniciar OpenCode** (`/exit` y `opencode`) para cargar agents, commands y skills nuevos
- [ ] **Crear Spec 001** con `/sdd-spec 001-portfolio-foundation "..."` para las pages y layout del frontend
- [ ] Implementar las tareas de spec 001 (pages, styles, lib, api/contact)
- [ ] Verificar build local: `cd portfolio-frontend && npm install && npm run build`
- [ ] `git add . && git commit && git push` → deploy Vercel + Render
- [ ] Añadir `/api/health` a la_nueva_era/app.py (healthcheck de Render)
- [ ] Verificar deploy: Vercel build en verde + Render `/api/health` responde
- [ ] Migrar datos de MySQL (PythonAnywhere) → PostgreSQL Neon schema `tfg`
- [ ] Verificar TFG end-to-end (React SPA + Flask API + Neon DB + Upstash)
- [ ] Spec 002: portfolio-backend/ con FastAPI + agentes IA en producción
- [ ] Spec 003: primer proyecto Node.js (schema `node_api`)
