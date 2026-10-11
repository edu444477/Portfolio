---
name: accessibility
description: Úsala cuando implementes o revises cualquier interfaz de usuario del portfolio - navegación por teclado, contraste, lectores de pantalla, prefers-reduced-motion. Requisito de la constitución, no opcional.
---

# Accesibilidad (WCAG 2.1 AA)

## Reglas de oro

- **HTML semántico primero**: `<button>` para acciones, `<a>` para navegación. Nunca `<div onClick>`.
- **Un solo `<h1>`** por página. Jerarquía sin saltos (`h2` → `h3`, nunca `h2` → `h4`).
- **Foco visible siempre**: `focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2`. Nunca elimines el outline sin reemplazarlo.
- **Contraste mínimo 4.5:1** para texto normal, 3:1 para texto grande (18px+ o 14px bold). Revisa light Y dark mode.

## Iconos

```tsx
// Icono dentro de botón con texto: decorativo
<Button><PlusIcon className="w-4 h-4" aria-hidden="true" /> Añadir</Button>

// Botón solo con icono: necesita nombre accesible
<button aria-label="Cerrar menú">
  <XMarkIcon className="w-6 h-6" aria-hidden="true" />
</button>

// Logo SVG: es contenido, necesita nombre
<svg role="img" aria-label="Logo de ED">...</svg>
```

## Formularios

```tsx
<Input label="Email" name="email" type="email" error={errors.email} required />
```

- Cada input tiene `<label htmlFor>` (el componente `Input` ya lo hace).
- Errores con `role="alert"` para que se anuncien.
- `aria-invalid="true"` cuando hay error, `aria-describedby` apuntando al mensaje.
- Nunca uses placeholder como sustituto de label.

## Navegación por teclado

- Menú móvil: `Escape` lo cierra, foco visible en el botón que lo abrió.
- Skip link: "Saltar al contenido principal" como primer elemento focusable.
- Orden de tabulación = orden visual. Nada de `tabindex` positivo.
- Modales y menús: `aria-expanded` en el trigger, `aria-controls` apuntando al panel.

## Movimiento

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Si añades animaciones con Tailwind (`animate-bounce`, `animate-slide-up`), comprueba que el bloque de arriba está en `global.css`.

## Checklist de revisión

- [ ] ¿Puedo recorrer toda la página solo con `Tab`?
- [ ] ¿El foco es visible en cada elemento interactivo?
- [ ] ¿Todos los botones solo-icono tienen `aria-label`?
- [ ] ¿El menú móvil se cierra con `Escape`?
- [ ] ¿Los inputs tienen label y sus errores se anuncian?
- [ ] ¿El contraste pasa en light y dark?
- [ ] ¿Hay un skip link al contenido principal?
- [ ] ¿Las animaciones respetan `prefers-reduced-motion`?

## Al terminar

Indica qué puntos del checklist has comprobado y cómo.