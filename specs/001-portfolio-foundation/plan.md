# Plan 001 — Portfolio Bilingüe

Plan técnico derivado de `spec.md`. Cada parte indica qué RF cubre.

---

## 1. Archivos y responsabilidades

| Archivo | Tipo | Responsabilidad | RF |
|---|---|---|---|
| `src/pages/[lang]/index.astro` | Página | Home: hero, about, experience, projects, tech, contact | RF-1, RF-3, RF-8, RF-12 |
| `src/pages/[lang]/projects/[slug].astro` | Página | Detalle de proyecto | RF-15, RF-16 |
| `src/pages/[lang]/404.astro` | Página | Página 404 con enlaces | RF-7 |
| `src/pages/[lang]/privacy.astro` | Página | Página de privacidad (RF-31) | RF-31 |
| `src/pages/api/contact.ts` | API | Endpoint serverless Web3Forms | RF-23, RF-24, RF-25, RF-26, RF-27 |
| `src/layouts/Layout.astro` | Layout | Shell HTML, header, footer, skip link, SEO, hreflang | RF-3, RF-8, RF-11, RF-12, RF-13, RFN-3, RFN-4, RFN-8, RFN-11 |
| `src/components/layout/Header.astro` | Componente | Navegación, selector de idioma, theme toggle, mobile menu | RF-3, RF-4, RF-5, RF-6, RF-8, RFN-3, RFN-4 |
| `src/components/layout/Footer.astro` | Componente | Contacto, enlaces, selector idioma, enlace privacidad | RF-8, RF-31 |
| `src/components/layout/ThemeProvider.tsx` | React island | Contexto de tema, persistencia localStorage | RF-28, RF-29, RF-30 |
| `src/components/ui/ThemeToggle.tsx` | React island | Botón alternar tema, aria-label bilingüe | RF-28, RFN-2 |
| `src/components/ui/LanguageToggle.tsx` | React island | Selector ES/EN, navega a URL con locale | RF-8, RFN-2 |
| `src/components/sections/Hero.astro` | Sección | Hero con nombre, rol, bio, CTAs | RF-1 |
| `src/components/sections/About.astro` | Sección | Perfil + datos identidad | RF-1, RF-2 |
| `src/components/sections/Experience.astro` | Sección | Timeline experiencia + formación | RF-18, RF-19 |
| `src/components/sections/Projects.astro` | Sección | Grid proyectos + tarjetas | RF-1, RF-14, RF-16, RF-17 |
| `src/components/sections/TechStack.astro` | Sección | Agrupación por source (cv/tfg/portfolio), niveles | RF-20, RF-21, RF-22 |
| `src/components/sections/Contact.astro` | Sección | Formulario + email visible, validación, estados | RF-23, RF-24, RF-25, RF-26, RF-27, RFN-2 |
| `src/lib/i18n.ts` | Librería | Diccionarios ES/EN, helper `t(key, lang)`, slugs traducidos | RF-8, RF-12, RFN-2 |
| `src/lib/constants.ts` | Librería | Identidad, contacto, enlaces, disponibilidad | RF-2 |
| `src/lib/utils.ts` | Librería | `cn()`, formateo fechas, slugs, truncado | RF-3, RF-15 |
| `src/content/config.ts` | Config | Schema Zod actualizado (tech.source, level 5 niveles) | RF-20, RF-21 |
| `src/content/tech/*.json` | Datos | 23 ficheros con `source` y `level` 5 valores | RF-20, RF-21, RF-22 |
| `src/content/projects/*.mdx` | Datos | TFG + portfolio + plantilla | RF-14, RF-15, RF-16 |
| `src/content/experience/*.mdx` | Datos | 4 empleos + 3 formaciones | RF-18, RF-19 |
| `src/styles/global.css` | Estilos | Tailwind directives, CSS variables, skip link, prefers-reduced-motion, dark mode class, foco visible, foco visible | RFN-1, RFN-3, RFN-4, RFN-5, RFN-6, RFN-11 |
| `astro.config.mjs` | Config | i18n routing, site URL, integrations | RF-8, RF-12, RF-13 |
| `vercel.json` | Config | Monorepo build, outputDirectory, headers | RF-13 |
| `portfolio-frontend/.env.example` | Config | Variables públicas actualizadas | — |

---

## 2. Componentes y lógica (React islands + lógica pura)

### 2.1 ThemeProvider (React island)
```tsx
// src/components/layout/ThemeProvider.tsx
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light'|'dark'>(() => {
    if (typeof window === 'undefined') return 'light';
    return (localStorage.getItem('theme') as 'light'|'dark') ||
           (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
    localStorage.setItem('theme', theme);
  }, [theme]);

  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}
```
- Props: `children: React.ReactNode`
- Estado: `theme` (localStorage + prefers-color-scheme)
- Efecto: alterna clase `dark` en `<html>`
- RF: 28, 29, 30

### 2.2 ThemeToggle (React island)
```tsx
// src/components/ui/ThemeToggle.tsx
export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const t = useTranslation(); // hook que lee i18n
  return (
    <button
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      aria-label={theme === 'light' ? t('theme.toDark') : t('theme.toLight')}
      className="..."
    >
      {theme === 'light' ? <MoonIcon /> : <SunIcon />}
    </button>
  );
}
```
- RF: 28, RFN-2 (aria-label bilingüe)

### 2.3 LanguageToggle (React island)
```tsx
// src/components/ui/LanguageToggle.tsx
export function LanguageToggle() {
  const { lang } = Astro.props; // 'es' | 'en'
  const t = useTranslation();
  const other = lang === 'es' ? 'en' : 'es';
  const href = `/${other}${Astro.url.pathname.replace(/^\/[a-z]{2}/, '') || '/'}`;

  return (
    <a href={href} className="..." aria-label={t('lang.switchTo', { lang: other })}>
      {other.toUpperCase()}
    </a>
  );
}
```
- Navega a URL con locale (recarga página) → RF-8
- Texto bilingüe via `i18n.ts` → RFN-2

### 2.4 i18n helper (lógica pura)
```ts
// src/lib/i18n.ts
export type Lang = 'es' | 'en';
export type Dict = Record<string, string>;

export const dicts: Record<Lang, Dict> = {
  es: { 'theme.toDark': 'Cambiar a modo oscuro', 'theme.toLight': 'Cambiar a modo claro', ... },
  en: { 'theme.toDark': 'Switch to dark mode', 'theme.toLight': 'Switch to light mode', ... },
};

export function t(key: string, lang: Lang, params?: Record<string, string>): string {
  let str = dicts[lang][key] || dicts.es[key] || key;
  if (params) Object.entries(params).forEach(([k,v]) => str = str.replace(`{${k}}`, v));
  return str;
}

export function getSlug(key: string, lang: Lang): string {
  // mapea 'proyectos' → 'projects' según locale
}
```
- Función pura, sin dependencias, testeable en Node
- RF-8, RF-12, RFN-2

### 2.5 Contact form (lógica pura + serverless)
```ts
// src/pages/api/contact.ts
export async function POST({ request }: APIContext) {
  const data = await request.formData();
  const name = data.get('name');
  const email = data.get('email');
  const subject = data.get('subject');
  const message = data.get('message');
  const lang = data.get('lang') || 'es';

  // Validación simultánea de 4 campos
  const errors: Record<string, string> = {};
  if (!name) errors.name = t('contact.error.required', lang);
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.email = t('contact.error.email', lang);
  if (!subject) errors.subject = t('contact.error.required', lang);
  if (!message) errors.message = t('contact.error.required', lang);

  if (Object.keys(errors).length > 0) {
    return new Response(JSON.stringify({ errors }), { status: 400 });
  }

  const web3formsUrl = 'https://api.web3forms.com/submit';
  const res = await fetch(web3formsUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      access_key: import.meta.env.WEB3FORMS_KEY,
      name, email, subject, message,
      from_name: 'Portfolio Contact',
    }),
  });

  if (!res.ok) {
    return new Response(JSON.stringify({ error: t('contact.error.failed', lang), email: 'eduardoorellanapomares@gmail.com' }), { status: 502 });
  }

  return new Response(JSON.stringify({ success: true, message: t('contact.success', lang) }), { status: 200 });
}
```
- Validación simultánea 4 campos → RF-24
- Email regex → RF-25
- Fallo Web3Forms → RF-26 (email fallback)
- Respuesta JSON con `aria-live` en cliente → RF-23
- RF-27: email visible en contacto (HTML estático)

---

## 3. Algoritmos clave (pseudocódigo)

### 3.1 Agrupación de tecnologías por source (precedencia cv > tfg > portfolio)
```
function groupTechBySource(techs: Tech[]): Record<string, Tech[]>:
  seen = new Set<string>()
  groups = { cv: [], tfg: [], portfolio: [] }
  for tech in techs sorted by (source precedence desc, level desc):
    if tech.name not in seen:
      groups[tech.source].push(tech)
      seen.add(tech.name)
  return groups
```
- RF-20, RF-21 (ordena por level desc dentro de grupo), RF-22 (precedencia)

### 3.2 Orden experiencia con tramos separados
```
function sortExperience(exp: ExperienceEntry[]):
  return exp.flatMap(e => {
    if e.hasMultipleTenures:
      return splitTenures(e) // devuelve 2 entradas con fechas de cada tramo
    else:
      return [e]
  }).sort((a,b) => b.endDate - a.endDate)
```
- RF-18

### 3.3 i18n routing (Astro)
```
Astro.config.mjs:
  i18n = { defaultLocale: 'es', locales: ['es', 'en'], prefixDefaultLocale: true }
  → genera /es/, /en/ y redirige / → /es/
```
- RF-8, RF-11, RF-12

### 3.4 Hreflang injection (Layout)
```
<head>
  <link rel="alternate" hreflang="es" href={url.replace('/en/', '/es/')} />
  <link rel="alternate" hreflang="en" href={url.replace('/es/', '/en/')} />
  <link rel="alternate" hreflang="x-default" href={url.replace('/en/', '/es/')} />
</head>
```
- RF-13

---

## 4. Interfaz (responsive, dark mode, estados)

| Componente | Breakpoints | Dark mode | Estados |
|---|---|---|---|
| Header | `< 768px` → drawer | `dark:` prefix en clases | `aria-expanded`, `aria-controls` |
| Hero | `min-h-screen`, `px-4 sm:px-6` | `bg-gradient-to-br from-primary-50 via-white to-dark-50 dark:from-dark-900` | — |
| Sections | `py-20 sm:py-28`, `mx-auto max-w-7xl` | `bg-white dark:bg-dark-800` | — |
| Project cards | `grid-cols-1 lg:grid-cols-2` | `dark:bg-dark-800 border-dark-700` | `hover:shadow-md` |
| Tech cards | `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4` | `dark:bg-dark-800` | `group-hover:border-primary-300` |
| Contact form | `space-y-5`, `w-full` | `dark:bg-dark-800` | `aria-invalid`, `aria-describedby`, `aria-live="polite"` |
| ThemeToggle | `p-2 rounded-lg` | `dark:bg-dark-800` | `aria-label` bilingüe |
| LanguageToggle | `px-3 py-1.5` | `dark:bg-dark-800` | `aria-label` bilingüe |
| Footer | `py-12`, `grid-cols-1 md:grid-cols-3` | `bg-dark-50 dark:bg-dark-900` | — |

- `prefers-reduced-motion`: desactiva animaciones en `global.css`
- `skip link`: `<a href="#main" class="sr-only focus:not-sr-only">Saltar al contenido</a>`
- Foco visible: `focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900`

---

## 5. Decisiones técnicas y alternativas descartadas

| Decisión | Justificación | Alternativa descartada |
|---|---|---|
| **i18n con recarga (no SPA)** | Cumple RF-8 reescrito + RF-12 (URLs propias). Astro nativo hace recarga, no requiere router cliente. | SPA con `next-intl` o `react-i18next` + client-side routing: añade JS innecesario, rompe RF-12 (URLs no propias), rompe RFN-1 (contenido principal requiere JS). |
| **Routing por locale con `prefixDefaultLocale: true`** | Genera `/es/`, `/en/`, redirige `/` → `/es/`. Cumple RF-11/RF-10/RF-12 nativamente en Astro 5. | Sin prefijo en default (`/en` pero `/`): rompe RF-11 (no hay locale en URL por defecto). |
| **Web3Forms en serverless function (api/contact.ts)** | Clave pública no viaja al navegador (RFN-7). Validación server-side + client-side (RF-24/25). Email fallback visible en HTML estático (RF-27). | Formspree/Resend directo desde cliente: expone clave o requiere backend propio. `mailto:`: UX pobre, no valida, no confirma. |
| **Content Collections para todo contenido dinámico** | Schema Zod valida en build (RF-20, RF-21). Type-safe en componentes. | JSON/MDX suelto sin schema: build pasa con datos rotos, viola RF-20. |
| **`source` enum en tech + precedencia** | RF-22 exige precedencia; enum en schema la hace type-safe. | String libre + lógica en componente: propenso a typos, no validadble en build. |
| **Level 5 valores fijos** | RF-21 exige escala fija y orden. Enum Zod lo garantiza. | String libre: "senior", "junior", etc. no ordenables. |
| **CSS variables + Tailwind `darkMode: 'class'`** | Cumple RF-28/29/30, RFN-5, RFN-11. Control total desde JS (`ThemeProvider`). | `media` query: no permite toggle manual (RF-28), no persiste (RF-29). |
| **`prefers-reduced-motion` en CSS** | RFN-11 lo exige. Un bloque CSS global cubre todo. | JS para detectar y desactivar: frágil, no cubre animaciones CSS puras. |
| **Web3Forms key en serverless env** | RFN-7 permite clave pública, pero no en el cliente. Serverless la inyecta en build. | Clave en `PUBLIC_` var: viaja al bundle, detectable en DevTools. |
| **`hxflang` en Layout.astro** | RF-13 exige marcado para buscadores. Astro genera URLs canónicas por locale. | Sitemap sin hreflang: Google no indexa versiones separadas. |

---

## 6. Estrategia de verificación

| RF/RFN | Verificación |
|---|---|
| RF-1 a RF-7, RF-14 a RF-19 | `npm run build` verde + revisión visual MCP Chrome DevTools (375px, 768px, 1440px) en ambos idiomas |
| RF-3 | MCP: click ancla → scroll suave + 80px offset visible |
| RF-4, RF-5, RF-6 | MCP (375px): menú hamburguesa abre/cierra, Escape cierra |
| RF-8, RF-12 | MCP: click selector idioma → navega a `/en/...`, URL cambia, HTML en inglés |
| RF-9, RF-10 | MCP: elige EN → recarga → persiste EN; cierra pestaña → abre → sigue EN |
| RF-11 | MCP: visita `/xx/` → redirige a `/es/` |
| RF-11/RF-10 precedencia | MCP: elige EN → visita `/` → redirige a `/en/` (no `/es/`) |
| RF-13 | Ver HTML: `<link rel="alternate" hreflang="es|en|x-default" ...>` presente |
| RF-14, RF-16 | MCP: proyectos orden descendente, TFG y portfolio en listado con ficha |
| RF-15 | MCP: click proyecto → detalle con descripción, stack, retos, aprendizajes, rol |
| RF-17 | MCP: proyecto sin `repoUrl`/`liveUrl` → no muestra enlace |
| RF-18 | MCP: experiencia orden inverso, VoIPer "actualidad", El Corte Inglés dos entradas |
| RF-20 | MCP: tres grupos cv/tfg/portfolio con encabezados |
| RF-21 | MCP: nivel visible, ordenado mayor a menor dentro de grupo |
| RF-22 | MCP: React aparece solo en grupo `cv` (precedencia) |
| RF-23 | MCP: envía formulario válido → `aria-live` confirma éxito |
| RF-24 | MCP: envía vacío → 4 errores simultáneos, sin envío |
| RF-25 | MCP: email inválido → error en campo email |
| RF-26 | Mock Web3Forms 502 → muestra error + email visible |
| RF-27 | Email `eduardoorellanapomares@gmail.com` visible en sección contacto (HTML) |
| RF-28,29,30 | MCP: toggle tema → alterna, persiste, default = OS |
| RF-31 | MCP: `/es/privacy` y `/en/privacy` existen, RGPD + Web3Forms |
| RFN-1 | Ver HTML inicial: contenido principal presente sin JS (View Source) |
| RFN-2 | MCP (ES/EN): 15 cadenas migradas, ninguna visible solo en un idioma |
| RFN-3 | MCP (Tab): foco visible en todos los interactivos, anillo 2px primary |
| RFN-4 | MCP (Tab primera tecla): "Saltar al contenido" aparece y salta a `<main>` |
| RFN-5 | Lighthouse Accessibility ≥95 (contraste ≥4.5:1 verificado) |
| RFN-6 | MCP (320px): sin scroll horizontal, todo legible |
| RFN-7 | Build: no secretos en bundle (grep `WEB3FORMS_KEY` en dist = 0) |
| RFN-8 | Ver HTML: `<title>`, `<meta name="description">`, `<link rel="canonical">`, `hreflang` |
| RFN-9 | `npm run build` exit code 0 |
| RFN-10 | Lighthouse CI: Performance/Accessibility/Best Practices/SEO ≥95 en ES y EN |
| RFN-11 | axe-core / Lighthouse Accessibility: 0 violations WCAG 2.1 AA |

### Herramientas
- **Build/Lint**: `npm run build && npm run lint` (debe pasar en cada tarea)
- **Visual/Interactivo**: MCP Chrome DevTools (375px, 768px, 1440px; ES/EN; light/dark)
- **Accesibilidad**: Lighthouse + axe-core (incluido en MCP)
- **Performance**: Lighthouse CI

---

## 7. Dependencias entre tareas (orden sugerido)

```
T1  Config i18n + routing          → RF-8,11,12,13, RFN-8
T2  Layout + Header + Footer       → RF-3,4,5,6,8, RFN-3,4,8,11
T3  ThemeProvider + ThemeToggle    → RF-28,29,30, RFN-2,11
T4  LanguageToggle                 → RF-8, RFN-2
T5  i18n dicts + constants.ts      → RF-2, RFN-2
T6  Hero + About                   → RF-1, RF-2
T7  Experience + Education         → RF-18,19
T8  Projects list + detail         → RF-14,15,16,17
T9  TechStack (source + level)     → RF-20,21,22
T10 Contact form + api/contact.ts  → RF-23..27, RFN-2,7
T11 Privacy page                   → RF-31
T12 404 page                       → RF-7
T13 Global CSS + a11y + dark mode  → RFN-1,3,4,5,6,11
T14 SEO + hreflang + sitemap       → RF-13, RFN-8,10
T15 Migración 15 cadenas hardcode  → RFN-2
T15 Build + Lighthouse + MCP final → RFN-9,10,11
```

Máximo 15 tareas, cada una ≤ 30 min, build verde entre tareas.

---

## 8. Criterios de "hecho" por tarea

Cada tarea en `tasks.md` llevará:
```
- [ ] **Tn. <Descripción>.** RF-x, RF-y
  - Hecho cuando: <comprobación verificable con comando o MCP>.
```

Ejemplo T1:
```
- [ ] **T1. Config i18n routing Astro + diccionarios base.** RF-8,11,12,13, RFN-8
  - Hecho cuando: `npm run build` verde; `/es/` y `/en/` sirven HTML; `<html lang="es|en">` correcto; `hreflang` presente en `<head>`.
```

---

Fin del plan. Listo para `/sdd-tasks 001-portfolio-foundation`.