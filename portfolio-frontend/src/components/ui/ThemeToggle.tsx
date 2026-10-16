import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';
import { clsx } from 'clsx';
import { useTheme } from '@/components/layout/ThemeProvider';
import { t, type Lang } from '@/lib/i18n';

interface ThemeToggleProps {
  lang: Lang;
}

export function ThemeToggle({ lang }: ThemeToggleProps) {
  // El estado vive en el store de tema; el toggle solo lo pide.
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className={clsx(
        'p-2 rounded-lg transition-all duration-200',
        'hover:bg-dark-100 dark:hover:bg-dark-800',
        'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900',
        'text-dark-600 dark:text-dark-400'
      )}
      aria-label={t(theme === 'light' ? 'theme.toDark' : 'theme.toLight', lang)}
      aria-pressed={theme === 'dark'}
    >
      {theme === 'light' ? (
        <MoonIcon className="w-5 h-5" aria-hidden="true" />
      ) : (
        <SunIcon className="w-5 h-5" aria-hidden="true" />
      )}
    </button>
  );
}