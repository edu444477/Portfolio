import { useState } from 'react';
import { GlobeAltIcon } from '@heroicons/react/24/outline';
import { clsx } from 'clsx';
import { t, type Lang } from '@/lib/i18n';

interface LanguageToggleProps {
  lang: Lang;
}

export default function LanguageToggle({ lang }: LanguageToggleProps) {
  const [isOpen, setIsOpen] = useState(false);
  const otherLang: Lang = lang === 'es' ? 'en' : 'es';
  const otherLabel = otherLang === 'es' ? 'ES' : 'EN';

  const toggleLanguage = () => {
    const currentPath = window.location.pathname;
    const newPath = currentPath.replace(/^\/(es|en)/, `/${otherLang}`);
    window.location.href = newPath || `/${otherLang}/`;
  };

  return (
    <div className="relative" onBlur={() => setIsOpen(false)}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        onClickCapture={() => toggleLanguage()}
        className={clsx(
          'p-2 rounded-lg transition-all duration-200',
          'text-dark-600 dark:text-dark-400',
          'hover:bg-dark-100 dark:hover:bg-dark-800',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900',
          'flex items-center gap-1.5'
        )}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-label={t('lang.switchTo', lang, { lang: otherLabel })}
      >
        <GlobeAltIcon className="w-5 h-5" aria-hidden="true" />
        <span className="hidden sm:inline font-medium text-sm">{otherLabel}</span>
        <svg
          className={clsx('w-4 h-4 transition-transform', isOpen && 'rotate-180')}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <ul
          role="listbox"
          className="absolute right-0 mt-1 w-20 bg-white dark:bg-dark-800 border border-dark-200 dark:border-dark-700 rounded-lg shadow-lg py-1 z-50 animate-slide-down"
        >
          {(['es', 'en'] as const).map((l) => (
            <li key={l} role="option" aria-selected={l === lang}>
              <button
                type="button"
                onClick={() => {
                  const currentPath = window.location.pathname;
                  const newPath = currentPath.replace(/^\/(es|en)/, `/${l}`);
                  window.location.href = newPath || `/${l}/`;
                }}
                className={clsx(
                  'w-full px-3 py-2 text-left text-sm font-medium transition-colors',
                  'focus:outline-none focus:bg-primary-50 dark:focus:bg-primary-900/30',
                  l === lang
                    ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300'
                    : 'text-dark-700 dark:text-dark-300 hover:bg-dark-50 dark:hover:bg-dark-700'
                )}
                aria-selected={l === lang}
              >
                {l.toUpperCase()}
              </button>
            </li>
          ))} 
        </ul>
      )}
    </div>
  );
}