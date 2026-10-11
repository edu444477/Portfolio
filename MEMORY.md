# MEMORY.md — Portfolio Personal

Memoria del proyecto entre sesiones. Máximo ~50 líneas.

## Estado actual (2026-10-11)

- **Infraestructura definida**: Vercel (frontend static) + Render (APIs) + Neon (PostgreSQL schemas) + Upstash (Redis)
- **Neon**: proyecto `rough-bar-22432276`, schemas `tfg`, `node_api`, `portfolio` creados. Usuario `tfg_user` con password hardcodeada en DB (⚠️ mover a variable de entorno)
- **Upstash**: DB `natural-rattler-221300`, REST URL + token disponibles
- **Render**: Web Service `la-nueva-era-api` creado, deploy desde GitHub (repo `edu444477/Portfolio`)
- **Vercel**: proyecto creado, deploy falló (repo vacío al momento). Root Directory: `portfolio-frontend`
- **Render**: servicio desplegado y **funcionando**. URL real: `https://la-nueva-era-api.onrender.com`. `/api/health` devuelve 200. Start command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 "app:app"`. Render NO lee render.yaml salvo Blueprint: el dashboard manda.
- **TFG (la_nueva_era/)**: Flask 3 + Flask-RESTful + SQLAlchemy + JWT + React 18 (TFG e-commerce). Deploy OK tras 3 bugs: dialecto psycopg2, /api/health, doble instancia de app. Falta migrar datos de MySQL → Neon y servir el build de React.
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

- **SQLAlchemy 2.x + `postgresql://`** → usa el driver psycopg v3. Con `psycopg2-binary` hay que forzar `postgresql+psycopg2://`. Error en runtime: `ModuleNotFoundError: No module named 'psycopg'`.
- **`current_app = create_app()` + gunicorn `app:create_app()`** → dos motores SQLAlchemy por proceso. Expón `app = create_app()` y arranca con `app:app`.
- **Vercel sin vercel.json en la raíz del monorepo** → `astro: command not found`. El vercel.json va en la raíz con `cd portfolio-frontend && npm run build`.
- **Vercel `rewrites: /(.*) → /index.html`** → secuestra todas las rutas y mata `/projects/*`. Un sitio estático de Astro no necesita rewrites.
- **Render root directory** → si Render dice que no existe, casi siempre es mayúscula/espacio/barra en el campo del dashboard. El repo estaba bien.
- **Render sin acceso al repo** → clona anónimamente pero no recibe webhooks: hay que reconnect o cada push exige Manual Deploy.
- **Content Collections `type: 'data'`** → un objeto por archivo. Un array en un solo `.json` rompe el sync (`Expected type "object", received "array"`). technologies va en 17 ficheros sueltos.
- **Neon connection string**: pooled lleva `-pooler` en el hostname y `channel_binding=require`. No quitarlo. Añadir siempre `&options=-csearch_path%3Dtfg`.

## Próximos pasos

- [ ] **Spec 001 aprobada**: `specs/001-portfolio-foundation/spec.md` en borrador (30 RF + 9 RFN, bilingüe es/en). Pendiente: clarificación, plan, tareas
- [ ] `/sdd-clarify 001-portfolio-foundation` → revisar la spec como QA antes de planear
- [ ] `/sdd-plan` + `/sdd-tasks` → tareas de implementación (pages, i18n, global.css, constants.ts, api/contact)
- [ ] `/sdd-implement 001-portfolio-foundation T1` → desbloquear el 404 de Vercel
- [ ] Migrar tablas MySQL (PythonAnywhere) → Neon schema `tfg` (`flask db upgrade` + exportar/importar datos)
- [ ] Servir el build de React del TFG: `templates/static/assets/` + `templates/index.html` ya están; falta comprobar que las rutas `/assets/...` resuelven en Flask
- [ ] Verificar CORS real desde `https://portfolio-delta-eight-yx2zi6pmny.vercel.app` contra la API
- [ ] Conectar Upstash: usar `REDIS_URL` para blacklist de JWT y rate limiting
- [ ] Spec 002: `portfolio-backend/` con FastAPI + agentes IA en producción
- [ ] Spec 003: primer proyecto Node.js (schema `node_api`)
