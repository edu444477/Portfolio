# Tasks 001 — Portfolio Bilingüe

Tareas derivadas de `plan.md`. Orden de dependencia, cada una ≤ 30 min, build verde entre tareas.

---

- [x] **T1. Config i18n routing Astro + diccionarios base.** RF-8, RF-11, RF-12, RF-13, RFN-8
  - Hecho cuando: `npm run build` verde; `/es/` y `/en/` sirven HTML; `<html lang="es|en">` correcto; etiquetas `hreflang` presentes en `<head>` de Layout; redirección `/` → `/es/` funciona; `/xx/` redirige a `/es/`.

- [x] **T2. Layout + Header + Footer (estructura + navegación + selector idioma).** RF-3, RF-4, RF-5, RF-6, RF-8, RFN-3, RFN-4, RFN-8, RFN-11
  - Hecho cuando: `npm run build` verde; header fijo con logo, nav, LanguageToggle, ThemeToggle; `< 768px` menú hamburguesa abre/cierra con click y Escape; anclas desplazan con scroll suave + 80px offset; footer con enlaces, email, LanguageToggle, enlace privacidad; skip link "Saltar al contenido" como primer focusable; foco visible en todos los interactivos; `<html lang>` correcto.

- [x] **T3. ThemeProvider + ThemeToggle (React island).** RF-28, RF-29, RF-30, RFN-2, RFN-11
  - Hecho cuando: `npm run build` verde; toggle alterna tema claro/oscuro; preferencia persiste en localStorage; default = `prefers-color-scheme`; `aria-label` bilingüe (ES/EN) en ThemeToggle; clase `dark` en `<html>` alterna; sin FOUC al cargar.

- [x] **T4. LanguageToggle (React island).** RF-8, RFN-2
  - Hecho cuando: `npm run build` verde; botón ES/EN en header y footer; click navega a URL con locale opuesto (recarga); `aria-label` bilingüe; texto del botón cambia según locale actual.

- [x] **T5. i18n diccionarios + constants.ts (identidad, contacto, enlaces).** RF-2, RFN-2
  - Hecho cuando: `npm run build` verde; `src/lib/i18n.ts` exporta `dicts.es`, `dicts.en`, `t(key, lang)`, `getSlug(key, lang)`; `src/lib/constants.ts` exporta `IDENTITY` (nombre, rol, bio, ubicación, teléfono, email, GitHub, LinkedIn, disponibilidad); claves cubren: hero, about, experience, projects, tech, contact, nav, footer, theme, form, errors, success.

- [x] **T6. Hero + About (secciones home).** RF-1, RF-2
  - Hecho cuando: `npm run build` verde; Hero muestra nombre, rol, bio, 2 CTAs (proyectos + contacto); About muestra "Mi historia" + perfil (nombre, rol, ubicación, disponibilidad, email) + skills destacados; textos via `constants.ts` + `i18n`; sin cadenas hardcodeadas.

- [ ] **T7. Experience + Education (timeline).** RF-18, RF-19
  - Hecho cuando: `npm run build` verde; Experience muestra 4 empleos en orden cronológico inverso: VoIPer (actualidad), A-Safe Digital, Elitech Lab, El Corte Inglés (dos tramos); cada uno con empresa, cargo, modalidad, fechas, descripción, logros, stack; Education muestra 3 formaciones con centro y periodo; datos desde Content Collections `experience`; El Corte Inglés aparece como dos entradas separadas.

- [ ] **T8. Projects list + detail (grid + página slug).** RF-14, RF-15, RF-16, RF-17
  - Hecho cuando: `npm run build` verde; Home muestra grid proyectos: TFG (destacado) + portfolio (destacado) + otros; orden descendente por fecha; tarjetas con título, descripción corta, stack (tags), badge estado, enlaces repo/demo solo si existen; click → `/es/projects/[slug]` o `/en/projects/[slug]` con detalle completo (descripción, stack, retos, aprendizajes, rol); slugs desde Content Collections `projects`.

- [ ] **T9. TechStack (agrupación por source + niveles).** RF-20, RF-21, RF-22
  - Hecho cuando: `npm run build` verde; tres grupos con encabezados: CV, TFG, Portfolio; dentro de cada grupo, tecnologías ordenadas por nivel (expert → learning); React aparece solo en grupo CV (precedencia cv > tfg > portfolio); cada tarjeta muestra nombre, nivel (badge), años opcional, descripción, enlace docs; datos desde Content Collections `tech` con campo `source` y `level` (5 valores).

- [ ] **T10. Contact form + api/contact.ts (Web3Forms).** RF-23, RF-24, RF-25, RF-26, RF-27, RFN-2, RFN-7
  - Hecho cuando: `npm run build` verde; sección contacto muestra email `eduardoorellanapomares@gmail.com` en texto plano; formulario con 4 campos (nombre, email, asunto, mensaje) + honeypot; validación client-side + server-side simultánea (4 errores acumulados); email regex; envío a Web3Forms via `api/contact.ts` (serverless); éxito → mensaje `aria-live="polite"` bilingüe; fallo 502 → error bilingüe + email visible; clave Web3Forms solo en server env (`WEB3FORMS_KEY`); no secretos en bundle cliente.

- [ ] **T11. Privacy page (ES/EN).** RF-31
  - Hecho cuando: `npm run build` verde; `/es/privacy` y `/en/privacy` existen; contenido RGPD mínimo + aviso Web3Forms; enlazada desde footer; navegable por teclado, contraste OK, sin cadenas hardcodeadas.

- [ ] **T12. 404 page (ES/EN).** RF-7
  - Hecho cuando: `npm run build` verde; `/es/404` y `/en/404` existen; mensaje amable + enlaces a home y proyectos; navegable, sin errores consola.

- [ ] **T13. Global CSS + a11y + dark mode + prefers-reduced-motion.** RFN-1, RFN-3, RFN-4, RFN-5, RFN-6, RFN-11
  - Hecho cuando: `npm run build` verde; `src/styles/global.css` con Tailwind directives, CSS variables (light/dark), skip link (`sr-only focus:not-sr-only`), foco visible (`focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900`), `prefers-reduced-motion` desactiva animaciones/transiciones; contraste ≥4.5:1 verificado en Lighthouse; 320px sin overflow horizontal; HTML inicial contiene contenido principal (View Source).

- [ ] **T14. SEO + hreflang + sitemap + meta tags.** RF-13, RFN-8, RFN-10
  - Hecho cuando: `npm run build` verde; cada página tiene `<title>`, `<meta name="description">`, `<link rel="canonical">`, `<link rel="alternate" hreflang="es|en|x-default">`; `astro.config.mjs` genera sitemap; Lighthouse SEO ≥95 en ES y EN.

- [ ] **T15. Migración 15 cadenas hardcodeadas + build final + Lighthouse + MCP final.** RFN-2, RFN-9, RFN-10, RFN-11
  - Hecho cuando: `npm run build` verde + `npm run lint` limpio; grep en `src/components` y `src/pages` no encuentra ninguna de las 15 cadenas listadas en RFN-2 (todas via `i18n`); Lighthouse CI ≥95 en Performance, Accessibility, Best Practices, SEO en ES y EN; axe-core 0 violations WCAG 2.1 AA; MCP Chrome DevTools: home, proyecto, 404, privacy en 375px/768px/1440px × ES/EN × light/dark; consola sin errores; consola sin secretos.

---

## Orden de ejecución sugerido

```
T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8 → T9 → T10 → T11 → T12 → T13 → T14 → T15
```

Cada tarea:
1. Implementa solo lo de esa tarea.
2. `npm run build && npm run lint` → debe pasar.
3. Si hay cambios visuales → MCP Chrome DevTools (375px, 768px, 1440px; ES/EN; light/dark).
4. Marca `[x]` en esta lista.
5. **PARA**. No encadenes tareas.

---

## Estado

- [x] T1
- [x] T2
- [x] T3
- [x] T4
- [x] T5
- [x] T6
- [ ] T7
- [ ] T8
- [ ] T9
- [ ] T10
- [ ] T11
- [ ] T12
- [ ] T13
- [ ] T14
- [ ] T15