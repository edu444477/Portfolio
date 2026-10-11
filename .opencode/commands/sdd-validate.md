---
description: SDD · Valida la spec RF por RF (build + Chrome DevTools)
agent: build
---

Recorre `specs/$1/spec.md` requisito por requisito. Para cada RF indica qué comprobación lo cubre y el resultado de ejecutarla.

- Frontend: `npm run build` + `npm run lint` + Chrome DevTools MCP (vista móvil 375px, dark mode).
- Backend: `pytest` + `curl /api/health`.

Si algún RF no está cubierto o falla, dilo claramente. NO arregles nada todavía.

Después comprueba los criterios de finalización y dame un veredicto: ¿la spec está cumplida?