# Specs (Spec-Driven Development)

Cada funcionalidad vive en su carpeta con tres archivos: `spec.md` (qué y por qué), `plan.md` (cómo), `tasks.md` (pasos verificables).

## Flujo

```
Constitución → Spec → Clarificación → Plan → Tareas → Implementación → Validación → Cambio
```

| Fase | Agente | Comando | Escribe |
|---|---|---|---|
| Constitución | plan | `/sdd-constitution` | `docs/constitution.md` |
| Especificación | plan | `/sdd-spec` | `spec.md` |
| Clarificación | plan | `/sdd-clarify` | (detecta, no escribe) |
| Planificación | plan | `/sdd-plan` | `plan.md` |
| Tareas | plan | `/sdd-tasks` | `tasks.md` |
| Implementación | build | `/sdd-implement` | código |
| Validación | build | `/sdd-validate` | (verifica, no arregla) |
| Cambio | plan | `/sdd-change` | `spec.md` primero |
| Estado | plan | `/sdd-status` | (solo lee) |

## Naming

`specs/NNN-nombre-kebab-case/` con NNN secuencial de 3 dígitos.

## Reglas

- Nada se implementa si no está en la spec activa.
- Si falta una decisión, se para y se pregunta al usuario.
- Un cambio de requisitos: primero la spec, luego el plan, luego las tareas, luego el código.
- Nunca se pasa de fase sin aprobación explícita del usuario.
- Los requisitos se escriben en EARS y deben ser verificables.

## Specs activas

| Spec | Estado | Descripción |
|---|---|---|
| _(pendiente de crear)_ | | Usa `/sdd-spec 001-nombre "descripción"` |
