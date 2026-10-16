import { clsx } from 'clsx';

interface TagProps {
  children: React.ReactNode;
  variant?: 'tech' | 'category' | 'status';
  removable?: boolean;
  onRemove?: () => void;
  className?: string;
}

export function Tag({ children, variant = 'tech', removable, onRemove, className }: TagProps) {
  const variants = {
    tech: 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300 border border-primary-200 dark:border-primary-800',
    category: 'bg-dark-100 text-dark-700 dark:bg-dark-700 dark:text-dark-300 border border-dark-200 dark:border-dark-600',
    status: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 border border-green-200 dark:border-green-800',
  };

  return (
    <span className={clsx(
      'inline-flex items-center gap-1.5 px-2.5 py-1 text-sm font-medium rounded-full',
      variants[variant],
      removable && 'cursor-pointer hover:opacity-80',
      className
    )}>
      {children}
      {removable && onRemove && (
        <button
          onClick={onRemove}
          className={clsx(
            'p-0.5 rounded-full transition-colors',
            'hover:bg-black/10 dark:hover:bg-white/10',
            'focus:outline-none focus:ring-2 focus:ring-primary-600'
          )}
          aria-label={`Eliminar ${children}`}
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </span>
  );
}