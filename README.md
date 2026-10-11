# Portfolio Personal

Portfolio multi-proyecto con metodología Spec-Driven Development y arquitectura de agentes IA.

## Qué es

- **Portfolio** (este repo): sitio estático con mi información, experiencia, tecnologías y proyectos.
- **Proyectos**: cada proyecto real vive en su carpeta con su propio backend y su propio schema de PostgreSQL.
- **Metodología IA**: agentes, subagentes, skills y comandos queigationan el desarrollo con specs.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | Astro 5 + React 18 (islands) + Tailwind CSS 3 + TypeScript strict |
| Iconos | Heroicons v2 |
| Fuentes | Inter Variable (self-hosted) |
| Backend TFG | Flask 3 + Flask-RESTful + SQLAlchemy + JWT |
| Base de datos | PostgreSQL (Neon) con schemas por proyecto |
| Caché / sesiones | Redis (Upstash) |
| Frontend hosting | Vercel |
| API hosting | Render |
| Desarrollo con IA | OpenCode (agents, skills, commands, SDD, MCP) |

## Estructura

```
Portfolio/
├── .opencode/              # Infraestructura IA
│   ├── agents/             # coordinator, planner, implementer, reviewer
│   ├── commands/           # /feature, /sdd-*
│   └── skills/             # sdd, astro-react-tailwind, python-backend, deployment, accessibility
├── docs/
│   ├── constitution.md     # Principios innegociables
│   └── deployment.md       # Guía de despliegue
├── specs/                  # Specs SDD versionadas
├── portfolio-frontend/     # Astro + React + Tailwind
├── la_nueva_era/           # TFG: Flask + React
├── AGENTS.md               # Instrucciones para agentes
├── MEMORY.md               # Memoria entre sesiones
├── opencode.json           # Config MCP
└── render.yaml             # Infrastructure as Code
```

## Desarrollo

### Frontend

```bash
cd portfolio-frontend
npm install
npm run dev        # http://localhost:4321
npm run build      # build de producción
npm run lint
```

### Backend (TFG)

```bash
cd la_nueva_era
python -m venv .venv
source .venv/Scripts/activate   # Windows
pip install -r requirements.txt
flask db upgrade
flask run
```

## Metodología de desarrollo (SDD)

Este proyecto usa **Spec-Driven Development**. Nada se implementa sin spec.

```
/sdd-spec 001-nombre "descripción"   → redacta la spec (te pregunta primero)
/sdd-clarify 001-nombre              → revisa la spec como QA
/sdd-plan 001-nombre                 → plan técnico
/sdd-tasks 001-nombre                → divide en tareas
/sdd-implement 001-nombre T1         → implementa UNA tarea
/sdd-validate 001-nombre             → valida RF por RF
/sdd-change 001-nombre "requisito"   → cambia la spec primero
/sdd-status 001-nombre               → dónde estamos
/feature "funcionalidad"             → cambio pequeño sin spec
```

### Agentes

| Agente | Rol |
|---|---|
| `coordinator` | Dirige el flujo SDD, transmite contexto entre fases |
| `planner` | Redacta spec, plan y tareas. No escribe código |
| `implementer` | Implementa UNA tarea. Verifica el build |
| `reviewer` | QA de specs y validación RF por RF. No modifica nada |

### Skills

| Skill | Cuándo |
|---|---|
| `sdd` | Trabajo con specs |
| `astro-react-tailwind` | Código en `portfolio-frontend/` |
| `python-backend` | Código en `la_nueva_era/` |
| `deployment` | Vercel, Render, Neon, Upstash, variables de entorno |
| `accessibility` | Cualquier interfaz de usuario |

## Despliegue

Ver `docs/deployment.md`. Resumen: `git push` y Vercel + Render despliegan automáticamente.

## Proyectos

| Proyecto | Stack | Backend | Estado |
|---|---|---|---|
| [La Nueva Era](https://github.com/edu444477/la_nueva_era) | Flask + React + PostgreSQL | Render | Completado |

## Licencia

Código propio. Todos los derechos reservados.
