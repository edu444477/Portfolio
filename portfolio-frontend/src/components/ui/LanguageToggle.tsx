import { GlobeAltIcon } from '@heroicons/react/24/outline';
import { clsx } from 'clsx';
import { t, localizePath, type Lang } from '@/lib/i18n';

interface LanguageToggleProps {
  lang: Lang;
  /** Ruta actual (p. ej. `/es/proyectos/`). Se traduce al otro locale. */
  pathname: string;
}

/**
 * Selector de idioma (RF-8).
 * Enlace real a la misma página en el otro locale: el HTML llega con el
 * `href` ya calculado desde el servidor, así que funciona sin JS y con
 * Cmd/Ctrl+click. No necesita estado, por eso no hay dropdown.
 */
export default function LanguageToggle({ lang, pathname }: LanguageToggleProps) {
  const otherLang: Lang = lang === 'es' ? 'en' : 'es';
  const otherLabel = otherLang === 'es' ? 'ES' : 'EN';

  return (
    <a
      href={localizePath(pathname, otherLang)}
      hrefLang={otherLang}
      lang={otherLang}
      data-testid="language-toggle"
      className={clsx(
        'p-2 rounded-lg transition-all duration-200 inline-flex items-center gap-1.5',
        'text-dark-600 dark:text-dark-400',
        'hover:bg-dark-100 dark:hover:bg-dark-800',
        'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900'
      )}
      aria-label={t('lang.switchTo', lang, { lang: otherLabel })}
    >
      <GlobeAltIcon className="w-5 h-5" aria-hidden="true" />
      <span className="hidden sm:inline font-medium text-sm">{otherLabel}</span>
    </a>
  );
}