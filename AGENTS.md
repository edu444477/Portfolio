# AGENTS.md — Portfolio Personal + Proyectos

Portfolio personal multi-proyecto desplegado en Vercel (frontend) + Render (APIs) + Neon (PostgreSQL) + Upstash (Redis).
Incluye múltiples proyectos reales (TFG "La Nueva Era", futuros proyectos Node.js, etc.) con metadata en Content Collections.

## Stack y estructura

- **Frontend**: Astro 5 + React 18 (islands) + Tailwind CSS 3 + Heroicons + TypeScript strict
  - `portfolio-frontend/src/content/` → Content Collections: projects, experience, tech (schema Zod)
  - `portfolio-frontend/src/components/ui/` → React islands (Button, Card, Badge, Input, ThemeToggle, Tag)
  - `portfolio-frontend/src/components/layout/` → Header, Footer, Hero, SEO, ThemeProvider
  - `portfolio-frontend/src/components/sections/` → About, Experience, Projects, TechStack, Contact
  - `portfolio-frontend/src/pages/` → index.astro, projects/[slug].astro, api/contact.ts
  - `portfolio-frontend/src/styles/global.css` → Tailwind directives + CSS variables (dark mode con clase)
- **Proyectos reales** en `projects/` (o `la_nueva_era/` en raíz):
  - `la_nueva_era/` → Flask 3 + Flask-RESTful + SQLAlchemy 2 + JWT + React 18 (TFG)
- **Infraestructura**: Vercel (static frontend) + Render (web services) + Neon (PostgreSQL schemas) + Upstash (Redis)

## Comandos

- **Frontend dev**: `cd portfolio-frontend && npm run dev`
- **Frontend build**: `cd portfolio-frontend && npm run build`
- **Frontend preview**: `cd portfolio-frontend && npm run preview`
- **Frontend lint**: `cd portfolio-frontend && npm run lint`
- **Frontend format**: `cd portfolio-frontend && npm run format`
- **TFG backend dev**: `cd la_nueva_era && flask run`
- **TFG backend prod**: `cd la_nueva_era && gunicorn --bind 0.0.0.0:8000 "app:create_app()"`
- **TFG migraciones**: `cd la_nueva_era && flask db upgrade`
- **TFG tests**: `cd la_nueva_era && pytest`

## Convenciones

- **Idioma**: Interfaz en español e inglés (bilingüe completo, routing por locale). Código en inglés, comentarios en español.
- **Tipado**: TypeScript strict en todo el frontend; Python type hints en backend
- **Estilos**: Tailwind CSS con clases de utilidad; CSS variables para theming
- **Iconos**: Heroicons v2 (outline para navegación, solid para acentos)
- **Fuentes**: Inter Variable self-hosted via @fontsource-variable/inter
- **Contenido**: Todo el contenido dinámico en Content Collections (MDX/JSON), nunca hardcodeado en componentes
- **Comentarios**: Solo donde aporten contexto, nunca obvios
- **Naming**: Componentes React en PascalCase, archivos .astro en PascalCase, utilidades en camelCase

## Reglas de dominio / trampas conocidas

- **Neon DATABASE_URL**: siempre termina con `&options=-csearch_path%3Dtfg` (schema del proyecto). Cambiar el schema = cambiar la DB.
- **Neon pooled vs direct**: usa pooled connection en web services (serverless), direct solo en migraciones/scripts.
- **Upstash REDIS_URL**: formato `redis://default:TOKEN@ENDPOINT:6379`. REST URL es para APIs HTTP, no para clientes Redis.
- **CORS_ORIGINS**: lista separada por comas con los dominios exactos (sin barra final). En producción: `https://portfolio-delta-eight-yx2zi6pmny.vercel.app`.
- **Render cold start**: 15 min de inactividad → sleep. El healthcheck `/api/health` mantiene el servicio despierto si se llama cada <10 min.
- **Vercel Root Directory**: en Vercel el root directory es `/` (raíz del repo). El `vercel.json` de la raíz configura el build del monorepo.
- **Render Root Directory**: para la API Flask es `la_nueva_era`, build command `pip install -r requirements.txt`.
- **Content Collections schema**: si añades un campo al schema en `content/config.ts`, TODOS los archivos MDX deben incluirlo o el build falla.
- **Tema oscuro**: usa clase `dark` en `<html>`, NO media queries. Tailwind `darkMode: 'class'`.

## Forma de trabajar

- **SDD obligatorio**: para cualquier funcionalidad nueva: spec → clarificación → plan → tareas → implementación (1 tarea) → validación.
- **Tarea a tarea**: implementa UNA tarea, ejecuta tests, marca en tasks.md, PARA. No encadenes tareas.
- **Cambios pequeños**: si el cambio cabe en un commit, no requiere spec. Usa `/feature`.
- **Resumo al terminar**: qué cambiaste, qué archivos, qué decide el usuario, qué falta.

## Límites

- ✅ **Siempre**: seguir SDD para funcionalidad nueva, actualizar MEMORY.md al terminar, mantener tipos estrictos, no hardcodear contenido en componentes, respetar schemas de Content Collections.
- ⚠ **Pregunta antes**: añadir dependencias npm/pip, cambiar schema de Content Collections, modificar estructura de DB, cambiar CORS_ORIGINS, añadir variables de entorno nuevas, cambiar domains.
- 🚫 **Nunca**: commitear secretos o claves API, modificar `la_nueva_era/` sin que lo pida, cambiar el schema de Neon sin avisar, deploy manual sin pasar por CI/CD.

## Verificación

- **Frontend**: `npm run build` sin errores + `npm run lint` limpio.
- **Visually**: MCP Chrome DevTools → abrir URL, probar responsive (375px, 768px, 1440px), verificar dark mode, revisar consola sin errores.
- **TFG API**: `curl http://localhost:8000/api/health` + verificar endpoints documentados.
- **Deploy**: Vercel dashboard (build logs) + Render dashboard (deploy logs) + healthcheck endpoint.
- **Antes de considerar terminado**: build pasa + lint pasa + verificación visual con Chrome DevTools MCP.

## Memoria

- Al empezar, lee `MEMORY.md` para conocer el estado del proyecto y decisiones tomadas.
- Al terminar una tarea, actualízalo: estado actual, decisiones importantes (con porqué) y errores a evitar.
- Mantenlo breve (máximo ~50 líneas): resume o elimina lo que ya no aporte.
- Si algo se convierte en una regla permanente, propón moverlo a `AGENTS.md` en lugar de dejarlo en la memoria.
- No guardes nunca datos sensibles (claves, tokens, datos personales).
