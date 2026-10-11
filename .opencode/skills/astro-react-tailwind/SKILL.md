---
name: astro-react-tailwind
description: Úsala siempre que escribas o modifiques código en portfolio-frontend/ - Astro, React islands, Tailwind CSS, Content Collections, Heroicons o el sistema de theming. Contiene los patrones y trampas de este proyecto.
---

# Astro + React + Tailwind en portfolio-frontend/

## Reglas de oro

- **Static-first**: React solo donde hay interactividad real. Si un componente no necesita estado ni efectos, es `.astro`, no `.tsx`.
- **Directivas de island**: usa `client:load` (necesita JS al cargar), `client:idle` (perezoso), `client:visible` (al hacer scroll). Nunca `client:only` sin motivo: rompe SSR.
- **Dark mode**: clase `dark` en `<html>`, NO media queries. Tailwind `darkMode: 'class'` ya está configurado.
- **ThemeToggle** (`@/components/ui/ThemeToggle`): maneja su propio estado y escribe en `localStorage` clave `theme`. No dupliques esa lógica.
- **Iconos**: Heroicons v2. `import { XIcon } from '@heroicons/react/24/outline'` (navegación) o `/24/solid` (acentos). Nunca SVG inline manual.
- **Fuentes**: Inter Variable vía `@fontsource-variable/inter`. Se importa en el Layout, no en cada componente.

## Content Collections (Astro)

- Schema Zod en `src/content/config.ts`. Define campos UNA vez y respétalos.
- **Trampa**: si añades un campo obligatorio al schema, TODOS los MDX de esa colección deben incluirlo o `npm run build` falla.
- Plantillas en `_template.mdx` (Astro las ignora por el prefijo `_`). Úsalas para crear nuevas entradas.
- Acceso: `await getCollection('projects')` devuelve entradas con `entry.data` (validado por Zod) y `entry.slug`.
- Nunca hardcodees contenido dinámico (proyectos, experiencia, stack tech) en componentes: va en Content Collections.

## Tailwind

- Colores: `primary` (escala 50-950) y `dark` (escala 50-950). No uses colores hardcodeados como `text-[#123456]`.
- Transiciones: `transition-all duration-200` como base en elementos interactivos.
- Responsive: mobile-first. Base sin prefijo, luego `sm:`, `md:`, `lg:`, `xl:`.
- Contenedores: `mx-auto max-w-7xl px-4 sm:px-6 lg:px-8`.

## Accesibilidad (requisito, no opcional)

- HTML semántico: `header`, `nav`, `main`, `section`, `footer`. Un solo `<h1>` por página.
- `aria-label` en botones solo con icono. `aria-hidden="true"` en iconos decorativos.
- Foco visible: `focus:outline-none focus:ring-2 focus:ring-primary-500`.
- Imágenes: `alt` descriptivo. SVG de logos: `role="img"` + `aria-label`.
- Formularios: `<label>` asociado por `htmlFor`, errores con `role="alert"`, `aria-invalid` en inputs con error.

## Verificación obligatoria

Antes de dar una tarea por hecha:

```bash
cd portfolio-frontend && npm run build && npm run lint
```

Si hay cambios visuales, además usa el MCP de Chrome DevTools para comprobar: 375px (móvil), 768px (tablet), 1440px (desktop); light y dark mode; consola sin errores.

## Checklist de revisión

- [ ] ¿Hay algún estado o efecto que justifique React? Si no, ¿es `.astro`?
- [ ] ¿Hay algún `client:*` innecesario?
- [ ] ¿El contenido dinámico está en Content Collections?
- [ ] ¿Todos los iconos vienen de Heroicons?
- [ ] ¿El dark mode funciona en TODOS los elementos nuevos?
- [ ] ¿Los botones solo-icono tienen `aria-label`?
- [ ] ¿Los inputs tienen `<label>` asociado?
- [ ] ¿`npm run build` pasa?

## Al terminar

Indica qué puntos del checklist has comprobado y cómo.