# Skills de este proyecto

Skills = instrucciones reutilizables que el agente carga cuando las necesita. A diferencia de los comandos (`/sdd-spec`), el agente puede usar una skill por iniciativa propia cuando detecta que la tarea lo requiere.

## Skills propias

| Skill | Cuándo se carga |
|---|---|
| `sdd` | Cualquier trabajo con `specs/`, `docs/constitution.md` o flujo SDD |
| `astro-react-tailwind` | Al escribir o modificar código en `portfolio-frontend/` |
| `python-backend` | Al escribir o modificar código Python en `la_nueva_era/` |
| `deployment` | Al tocar Vercel, Render, Neon, Upstash, variables de entorno o dominios |
| `accessibility` | Al implementar o revisar cualquier interfaz de usuario |

## Skills de comunidad (instalables)

Vienen del ecosistema [skills.sh](https://skills.sh). Se instalan de forma modular para no ensuciar el contexto principal:

```bash
# Instalar el paquete agent-skills
npx skills add vercel-labs/agent-skills

# Instalar una skill concreta
npx skills add https://github.com/anthropics/skills --skill frontend-design
```

| Skill | Origen | Para qué |
|---|---|---|
| `find-skills` | Vercel | Busca e instala skills cuando necesitas una capacidad nueva |
| `frontend-design` | Anthropic | Interfaces con diseño cuidado y profesional |
| `web-design-guidelines` | Vercel | Revisa accesibilidad, UX y diseño de una interfaz existente |
| `grill-me` | Matt Pocock | Te hace preguntas sobre tu plan hasta cubrir todos los casos |
| `systematic-debugging` | Jesse Vincent | Depura con método: reproducir, aislar, formular hipótesis, verificar |

## Cómo se usa una skill

En OpenCode, el agente carga la skill automáticamente si su `description` coincide con la tarea. También puedes invocarla manualmente:

```
@astro-react-tailwind
@sdd
@deployment
```

Para forzar su uso en una petición concreta, menciona la skill en el prompt:

```
@frontend-design con lo que sabes mejora el diseño de la home
```

## Instalación con alcance

Al instalar una skill puedes elegir:
- **Alcance**: global (`~/.agents/skills/`) o proyecto (`.agents/skills/` en el repo).
- **Agentes**: para qué agentes instalarla (Claude Code, OpenCode, etc.).

Recomendación: instala las de comunidad en alcance **proyecto** para que el repo sea reproducible, y las personales en **global**.