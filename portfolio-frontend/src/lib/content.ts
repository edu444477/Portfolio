/**
 * Selección de contenido por idioma.
 *
 * Convención: cada colección tiene subcarpetas por idioma,
 * `projects/localized-es/la_nueva_era.mdx` y `projects/localized-en/...`.
 * El slug de Astro conserva la ruta, así que el idioma es el primer
 * segmento y el slug público es el resto.
 *
 * OJO: el sufijo en el NOMBRE del fichero (`la_nueva_era.en.mdx`) NO sirve,
 * Astro concatena el punto y devuelve `la_nueva_eraen`.
 *
 * El schema de Content Collections NO cambia: cada fichero sigue teniendo
 * los mismos campos, ya escritos en su idioma.
 */

import type { CollectionEntry } from 'astro:content';
import type { Lang } from '@/lib/i18n';

const LOCALES = ['es', 'en'] as const;
const LOCALE_DIR = 'localized-';

function isLocale(value: string): value is Lang {
  return (LOCALES as readonly string[]).includes(value);
}

/** `localized-es/la_nueva_era` -> `la_nueva_era` */
export function baseSlug(slug: string): string {
  const [first, ...rest] = slug.split('/');
  if (rest.length > 0 && first.startsWith(LOCALE_DIR) && isLocale(first.slice(LOCALE_DIR.length))) {
    return rest.join('/');
  }
  return slug;
}

/** El idioma va en la carpeta; sin carpeta se asume español. */
function localeOf(entry: CollectionEntry): Lang {
  const [first] = entry.slug.split('/');
  if (first && first.startsWith(LOCALE_DIR)) {
    const candidate = first.slice(LOCALE_DIR.length);
    if (isLocale(candidate)) return candidate;
  }
  return 'es';
}

/**
 * Entradas de una colección para un idioma, con el slug público ya limpio.
 * Si un idioma no tiene traducción, cae al español para no dejar huecos.
 */
export function byLocale<T extends CollectionEntry>(
  entries: readonly T[],
  lang: Lang,
): (T & { slug: string })[] {
  const localized = entries
    .filter((entry) => localeOf(entry) === lang)
    .map((entry) => ({ ...entry, slug: baseSlug(entry.slug) }));

  if (lang === 'es') return localized;

  const translatedSlugs = new Set(localized.map((entry) => entry.slug));
  const fallback = entries
    .filter((entry) => localeOf(entry) === 'es' && !translatedSlugs.has(baseSlug(entry.slug)))
    .map((entry) => ({ ...entry, slug: baseSlug(entry.slug) }));

  return [...localized, ...fallback];
}

/** Una entrada concreta por idioma (para la página de detalle). */
export function findByLocale<T extends CollectionEntry>(
  entries: readonly T[],
  lang: Lang,
  slug: string,
): (T & { slug: string }) | undefined {
  const exact = entries.find((entry) => localeOf(entry) === lang && baseSlug(entry.slug) === slug);
  if (exact) return { ...exact, slug: baseSlug(exact.slug) };

  const fallback = entries.find((entry) => localeOf(entry) === 'es' && baseSlug(entry.slug) === slug);
  return fallback ? { ...fallback, slug: baseSlug(fallback.slug) } : undefined;
}

export { localeOf };