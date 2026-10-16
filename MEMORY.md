# MEMORY.md — Portfolio Personal

Memoria del proyecto entre sesiones. Máximo ~50 líneas.

## Estado actual (2026-10-16)

- **Spec 001 (Portfolio bilingüe)**: T1-T15 COMPLETADAS. La web está terminada: home, 2 proyectos con detalle, privacidad, 404, todo en ES/EN.
- **Frontend (portfolio-frontend/)**: `npm run build` y `npm run lint` limpios. Consola del navegador sin errores ni 404. Verificado en Chrome a 375/768/1440px, light y dark.
- **Tema**: store único en `src/lib/theme.ts` (localStorage + prefers-color-scheme) leído con `useSyncExternalStore`. `ThemeProvider.tsx` exporta el hook `useTheme()`; ya no es un Provider de contexto.
- **PENDIENTE PARA QUE FUNCIONE EL FORMULARIO**: definir `WEB3FORMS_KEY` en las variables de entorno de Vercel (documentada en `.env.example`). Sin ella, `POST /api/contact` devuelve 500 y el visitante ve el email en texto plano.
- **TFG (la_nueva_era/)**: desplegado y funcionando en `https://la-nueva-era-api.onrender.com`. `/api/health` = 200. Start command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 "app:app"`. Falta migrar datos MySQL → Neon y servir el build de React.
- **Neon**: proyecto `rough-bar-22432276`, schemas `tfg`, `node_api`, `portfolio`. Usuario `tfg_user` con password en DB (⚠️ mover a variable de entorno).
- **Upstash**: DB `natural-rattler-221300`. Sin conectar (blacklist JWT + rate limiting pendientes).
- **Render**: Web Service `la-nueva-era-api` desplegado desde GitHub (`edu444477/Portfolio`). Render NO lee render.yaml salvo Blueprint: el dashboard manda.
- **Vercel**: deploy automático desde la raíz del repo (monorepo). vercel.json en raíz, NO en portfolio-frontend.

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
- **Astro: en `.astro` conviven DOS atributos que NO son intercambiables.** Elementos HTML → `class=`. Componentes React (Heroicons) → `className=`, porque reciben props de React. Usar `class=` en un Heroicon deja el SVG sin tamaño y se estira al 100% del contenedor (parece un icono gigante en medio de la página). Usar `className=` en HTML no aplica estilo. Los 4 fallos juntos bannedron toda la web sin estilos ni errores visibles.
- **No escribir JSX de React en plantillas `.astro`**: `return (...)`, `key={}`, `<Component/>` dentro de `.map()` no existen en Astro. Usa `{lista.map(x => (<li>...</li>))}` sin `return`, y `key` es opcional.
- **Los islands de Astro se renderizan FUERA del árbol de React.** Un `<ContextProvider client:load>` en el Layout no alcanza a `Header`/`Footer`: Astro los serializa aparte y salta con "must be used within a ThemeProvider". Para estado compartido entre islands usar un store exterior (como `src/lib/theme.ts`), no contexto.
- **Para leer localStorage en React sin hydration mismatch**: `useSyncExternalStore`, no `useState` + `useEffect` con `setMounted(true)`. La regla `react-hooks/set-state-in-effect` de plugin v7 lo marca como error.
- **ESLint 9 = flat config**: `eslint.config.mjs`, y `--ext` ya no existe (el script es `eslint .`). `eslint-plugin-astro@3.x` exige ESLint ≥10 → con ESLint 9 fijar `eslint-plugin-astro@1.3.1`. Añadir `.vercel/**` a `ignores`, si no lint escanea 1000+ errores del build.
- **Con `output: 'server'` hace falta un adapter** (`@astrojs/vercel@8.0.0` para Astro 5; la v11 exige Astro 7) y va en `adapter:`, NO dentro de `integrations: []`. El build pasa a generar `dist/client` + `.vercel/output`, y `astro preview` ya no sirve: usar `http-server dist/client`.
- `tsc --noEmit` directo no entiende ficheros `.astro`: da falsos errores. Para tipos reales usar `astro check`.

## Próximos pasos

- [ ] **Definir `WEB3FORMS_KEY` en Vercel** para que el formulario de contacto funcione de verdad
- [ ] **Desplegar y verificar en producción** (`https://portfolio-delta-eight-yx2zi6pmny.vercel.app`): comprobar que las páginas prerenderizadas se sirven y que la función `/api/contact` responde
- [ ] Arreglar los barrels `src/components/*/index.ts`: exportan `{ Header }` de un módulo con `export default` → error TS. Usar default export o `export { default as X }`
- [ ] Traducir el contenido de los proyectos yempleos a EN (ahora el interfaz está en ambos idiomas pero el texto largo de Content Collections solo existe en ES)
- [ ] Migrar tablas MySQL (PythonAnywhere) → Neon schema `tfg`
- [ ] Servir el build de React del TFG (`templates/static/assets/` ya están; comprobar que `/assets/...` resuelven en Flask)
- [ ] Verificar CORS real desde `https://portfolio-delta-eight-yx2zi6pmny.vercel.app` contra la API
- [ ] Conectar Upstash: `REDIS_URL` para blacklist de JWT y rate limiting
- [ ] Spec 002: `portfolio-backend/` con FastAPI + agentes IA en producción
- [ ] Spec 003: primer proyecto Node.js (schema `node_api`)
