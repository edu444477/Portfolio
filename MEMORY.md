# MEMORY.md — Portfolio Personal

Memoria del proyecto entre sesiones. Máximo ~50 líneas.

## Estado actual (2026-10-16)

- **Spec 001 (Portfolio bilingüe)**: aprobada y en ejecución. Tareas hechas: T1, T2, T3, T5, T6. Pendientes: T4 (LanguageToggle island) y T7→T15.
- **Frontend (portfolio-frontend/)**: rutas `/es/` y `/en/` generadas. Layout + Header + Footer + ThemeToggle + ThemeProvider + i18n + constants + Hero + About funcionando y bilingües. Build verde.
- **TFG (la_nueva_era/)**: desplegado y funcionando en `https://la-nueva-era-api.onrender.com`. `/api/health` = 200. Start command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 "app:app"`. Falta migrar datos MySQL → Neon y servir el build de React.
- **Neon**: proyecto `rough-bar-22432276`, schemas `tfg`, `node_api`, `portfolio`. Usuario `tfg_user` con password en DB (⚠️ mover a variable de entorno).
- **Upstash**: DB `natural-rattler-221300`. Sin conectar (blacklist JWT + rate limiting pendientes).
- **Render**: Web Service `la-nueva-era-api` desplegado desde GitHub (`edu444477/Portfolio`). Render NO lee render.yaml salvo Blueprint: el dashboard manda.
- **Vercel**: deploy automático desde la raíz del repo (monorepo). vercel.json en raíz, NO en portfolio-frontend.
- **.opencode/ COMPLETO**: 4 agents, 10 commands, 5 skills propias. Docs: docs/constitution.md, docs/deployment.md.

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
- **Astro: `Astro.props` NO lleva los params de ruta.** En `src/pages/[lang]/...` el idioma se lee de `Astro.params.lang`. Usar `Astro.props` da `undefined` y revienta con `Cannot read properties of undefined` al indexar `dicts[lang]`.
- **Astro usa `class=`, no `className=`.** `className` solo es válido en componentes React (.tsx). En `.astro` se renderiza como atributo vacío → la sección sale sin estilos y no hay error visible. Ojo con Contact/Experience/Projects/TechStack, que aún tienen `className` (pendiente en sus tareas).
- **`npm run lint` está roto**: ESLint 9 requiere `eslint.config.mjs` (flat config) y no acepta `--ext`. El script existe pero falla siempre. Arreglar en T15 o crear el config.
- `tsc --noEmit` directo no entiende ficheros `.astro`: da falsos errores. Para tipos reales usar `astro check`. Los errores preexistentes de barrels `index.ts` (imports con nombre vs default) son conocidos.
- **`src/styles/global.css` NO existe todavía** (pendiente de T13). Tailwind ya inyecta sus utilidades vía @astrojs/tailwind, así que el sitio tiene estilos, pero sin el CSS global faltan variables, skip link y prefers-reduced-motion.

## Próximos pasos

- [ ] **T4. LanguageToggle** (React island): el componente existe en `components/ui/LanguageToggle.tsx` y ya se usa en Header, pero T4 no está marcada ni verificada (idioma del botón, navegación, aria-label bilingüe)
- [ ] **T7. Experience + Education** (timeline). Ojo: `Experience.astro` tiene `className=` → sin estilos, y las claves nav están sin traducir (`nav.inicio` literal en el Header)
- [ ] **T8. Projects list + detail** + arreglar `className` en Projects.astro
- [ ] **T9. TechStack** + `className` en TechStack.astro
- [ ] **T10. Contact form + api/contact.ts** + `className` en Contact.astro
- [ ] **T11-T12.** Páginas privacy y 404 ES/EN
- [ ] **T13.** Crear `src/styles/global.css` (Tailwind directives, CSS variables, skip link, foco visible, prefers-reduced-motion)
- [ ] **T14-T15.** SEO/hreflang/sitemap, migración de cadenas restantes, Lighthouse + axe
- [ ] Arreglar `npm run lint`: crear `eslint.config.mjs` para ESLint 9 flat config
- [ ] Arreglar SVG corrupto en `components/ui/BrandIcons.tsx` (línea 9: hay un `path` de GitHub pegado dentro de otro → error `<path> attribute d` en consola)
- [ ] Añadir `favicon.ico` (404 en consola)
- [ ] Migrar tablas MySQL (PythonAnywhere) → Neon schema `tfg`
- [ ] Servir el build de React del TFG (`templates/static/assets/` ya están; comprobar que `/assets/...` resuelven en Flask)
- [ ] Verificar CORS real desde `https://portfolio-delta-eight-yx2zi6pmny.vercel.app` contra la API
- [ ] Conectar Upstash: `REDIS_URL` para blacklist de JWT y rate limiting
- [ ] Spec 002: `portfolio-backend/` con FastAPI + agentes IA en producción
- [ ] Spec 003: primer proyecto Node.js (schema `node_api`)
