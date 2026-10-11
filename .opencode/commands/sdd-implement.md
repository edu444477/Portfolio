---
description: SDD · Implementa UNA tarea, build verificable (uso - /sdd-implement 002-nombre T3)
agent: build
---

Implementa SOLO la tarea $2 de `specs/$1/tasks.md`, siguiendo `specs/$1/plan.md`, `docs/constitution.md`, `AGENTS.md` y la skill sdd.

1. Si la tarea es de lógica, escribe primero una comprobación que falle (test o build en rojo).
2. Escribe el código hasta que pase.
3. Ejecuta `npm run build` (frontend) o `pytest` (backend) y muéstrame el resultado.
4. Si hay cambios visuales, verifica con Chrome DevTools MCP (incluida vista móvil 375px y dark mode).
5. Marca $2 como hecha en `tasks.md` e indica qué RF cubre.

Después PÁRATE. No empieces la siguiente tarea.