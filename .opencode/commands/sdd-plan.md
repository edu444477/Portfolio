---
description: SDD · Genera el plan técnico de una spec aprobada
agent: plan
---

Lee docs/constitution.md, AGENTS.md y `specs/$1/spec.md`. Usa la skill sdd.
NO escribas código.

Genera `specs/$1/plan.md` con:

- Archivos que se crean o modifican y la responsabilidad de cada uno.
- Componentes/lógica: para React, qué islands y qué props; para lógica pura, funciones con parámetros explícitos.
- Algoritmos clave en pseudocódigo.
- Cómo se pinta en la interfaz (responsive, dark mode, estados).
- Decisiones técnicas justificadas (y su alternativa descartada).
- Estrategia de verificación: `npm run build`, `npm run lint`, Chrome DevTools MCP (incluida vista móvil 375px).

Todo debe respetar la constitución y cubrir todos los RF. Marca qué RF cubre cada parte.
Si la spec no está aprobada o tiene dudas abiertas, para y avísame.