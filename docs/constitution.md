# Constitución — Portfolio Personal

Principios innegociables. Toda spec, plan y tarea debe cumplirlos.

1. **Static-first**: El frontend es HTML estático por defecto. React solo donde hay interactividad real (islands). Cero JS no justificado.
2. **La spec manda**: Nada se implementa si no está en la spec activa. Si falta una decisión, se para y se pregunta al usuario.
3. **Tipos estrictos**: TypeScript strict en todo el frontend. Python type hints en backend. Schemas Zod para todo contenido externo.
4. **Aislamiento por schema**: Cada proyecto usa su propio schema de PostgreSQL (`tfg`, `node_api`, `portfolio`). Nunca prefijos de tabla: schemas reales con permisos por usuario.
5. **Deploy reproducible**: Todo servicio tiene config declarativa (`render.yaml`, `vercel.json`, `.env.example`). Nunca secretos hardcodeados: solo variables de entorno.
6. **Accesibilidad y rendimiento**: WCAG 2.1 AA mínimo (contraste, foco visible, navegación por teclado, semántica HTML). Lighthouse ≥95 en las 4 categorías.

## Principios de la arquitectura

- **Desacoplamiento**: Frontend, backend y base de datos se despliegan y escalan independientemente.
- **Providers(IdC)**: Vercel para static, Render para APIs, Neon para PostgreSQL, Upstash para Redis.
- **Monorepo**: Un solo repo GitHub con todo (frontend + proyectos + infraestructura + docs IA).
- **IA-as-code**: La metodología de desarrollo (agents, skills, commands, specs) vive en el repo y es ejecutable.

## Qué NO hacemos

- No frameworks JSglobals (React global no, solo islands).
- No base de datos embebida en el frontend.
- No secretos en el repositorio (ni en examples).
- No commits directos a `main` sin pasar por build de CI (aunque GitHub Actions no esté activo aún, el build local debe pasar).
