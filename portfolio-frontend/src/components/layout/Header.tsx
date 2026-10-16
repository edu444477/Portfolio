import { useState, useEffect, useRef } from 'react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { clsx } from 'clsx';
import { ThemeToggle } from '@/components/ui';
import LanguageToggle from '@/components/ui/LanguageToggle';
import { t, localizePath, type Lang } from '@/lib/i18n';

const navigation = [
  { key: 'inicio', i18n: 'nav.inicio' },
  { key: 'experiencia', i18n: 'nav.experiencia' },
  { key: 'proyectos', i18n: 'nav.proyectos' },
  { key: 'tecnologias', i18n: 'nav.tecnologias' },
  { key: 'contacto', i18n: 'nav.contacto' },
] as const;

interface HeaderProps {
  lang: Lang;
  pathname: string;
}

export default function Header({ lang, pathname }: HeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const mobileMenuRef = useRef<HTMLDivElement>(null);
  const lastFocusedRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false);
        lastFocusedRef.current?.focus();
      }
    };
    if (mobileMenuOpen) {
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  useEffect(() => {
    if (mobileMenuOpen && mobileMenuRef.current) {
      lastFocusedRef.current = document.activeElement as HTMLElement;
      mobileMenuRef.current.focus();
    }
  }, [mobileMenuOpen]);

  // RF-3: las secciones viven en la home, así que los enlaces son anclas
  // (`/es/#proyectos/`), no rutas sueltas que darían 404.
  const homeHref = localizePath('/', lang);
  const anchorHref = (key: string) => `${homeHref}#${key}`;

  return (
    <header
      className={clsx(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        scrolled
          ? 'bg-white/90 dark:bg-dark-950/90 backdrop-blur-md shadow-sm border-b border-dark-200 dark:border-dark-800'
          : 'bg-transparent'
      )}
      role="banner"
    >
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8" aria-label={t('nav.primary', lang)}>
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <a href={anchorHref('inicio')} className="flex items-center gap-2 text-xl font-bold text-dark-900 dark:text-dark-100" aria-label={`ED — ${t('nav.inicio', lang)}`}>
              <svg className="w-8 h-8 text-primary-600 dark:text-primary-400" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true">
                <path d="M16 2L4 8v16l12 6 12-6V8L16 2zm0 2.5L25.5 9 16 13.5 6.5 9 16 4.5zM6 10.5l9 4.5v11l-9-4.5v-11zm11 11V15l9-4.5v11l-9 4.5z"/>
              </svg>
              <span>ED</span>
            </a>
          </div>

          <div className="hidden md:flex md:items-center md:gap-8">
            <nav aria-label={t('nav.primary', lang)}>
              <ul className="flex items-center gap-8">
                {navigation.map((item) => (
                  <li key={item.key}>
                    <a
                      href={anchorHref(item.key)}
                      className="text-sm font-medium text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                    >
                      {t(item.i18n, lang)}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
            <LanguageToggle lang={lang} pathname={pathname} />
            <ThemeToggle lang={lang} />
          </div>

          <div className="flex md:hidden items-center gap-4">
            <LanguageToggle lang={lang} pathname={pathname} />
            <ThemeToggle lang={lang} />
            <button
              type="button"
              className="p-2 rounded-lg text-dark-600 dark:text-dark-400 hover:bg-dark-100 dark:hover:bg-dark-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-menu"
              aria-label={t(mobileMenuOpen ? 'nav.closeMenu' : 'nav.openMenu', lang)}
            >
              {mobileMenuOpen ? (
                <XMarkIcon className="w-6 h-6" aria-hidden="true" />
              ) : (
                <Bars3Icon className="w-6 h-6" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div
            ref={mobileMenuRef}
            id="mobile-menu"
            className="md:hidden py-4 border-t border-dark-200 dark:border-dark-700 animate-slide-down"
            role="navigation"
            aria-label={t('nav.mobile', lang)}
            tabIndex={-1}
          >
            <nav aria-label={t('nav.mobile', lang)}>
              <ul className="flex flex-col gap-4">
                {navigation.map((item) => (
                  <li key={item.key}>
                    <a
                      href={anchorHref(item.key)}
                      className="px-2 py-2 text-base font-medium text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 rounded-lg hover:bg-dark-100 dark:hover:bg-dark-800 transition-colors"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      {t(item.i18n, lang)}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
            <div className="pt-2 flex justify-center">
              <LanguageToggle lang={lang} pathname={pathname} />
              <ThemeToggle lang={lang} />
            </div>
          </div>
        )}
      </nav>
    </header>
  );
}