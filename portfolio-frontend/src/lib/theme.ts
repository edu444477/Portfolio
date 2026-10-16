/**
 * Store del tema (RF-28, RF-29, RFN-2).
 *
 * Fuente única de verdad: `localStorage['theme']` + `prefers-color-scheme`.
 * ThemeProvider y ThemeToggle lo comparten, así no duplican ni la key ni
 * el toggle de la clase `dark` en <html>.
 *
 * Se lee con useSyncExternalStore y no con useState + useEffect: así el
 * servidor renderiza el snapshot por defecto y el cliente hidrata con el
 * valor real sin mismatch ni cascada de renders.
 */

export type Theme = 'light' | 'dark';

const STORAGE_KEY = 'theme';

type Listener = () => void;

const listeners = new Set<Listener>();

function emit(): void {
  listeners.forEach((listener) => listener());
}

function systemTheme(): Theme {
  return typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}

/** Valor por defecto para SSR: siempre claro. El cliente corrige al hidratar. */
function serverTheme(): Theme {
  return 'light';
}

export function getSnapshot(): Theme {
  if (typeof window === 'undefined') return serverTheme();
  return (localStorage.getItem(STORAGE_KEY) as Theme | null) ?? systemTheme();
}

function applyTheme(theme: Theme): void {
  document.documentElement.classList.toggle('dark', theme === 'dark');
}

export function setTheme(theme: Theme): void {
  localStorage.setItem(STORAGE_KEY, theme);
  applyTheme(theme);
  emit();
}

export function toggleTheme(): Theme {
  const next = getSnapshot() === 'light' ? 'dark' : 'light';
  setTheme(next);
  return next;
}

export function subscribe(listener: Listener): () => void {
  listeners.add(listener);

  // Si el visitante cambia la preferencia del sistema y no ha elegido un
  // tema manualmente, la vista sigue al sistema.
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  const onSystemChange = (event: MediaQueryListEvent) => {
    if (localStorage.getItem(STORAGE_KEY)) return;
    applyTheme(event.matches ? 'dark' : 'light');
    emit();
  };
  media.addEventListener('change', onSystemChange);

  return () => {
    listeners.delete(listener);
    media.removeEventListener('change', onSystemChange);
  };
}

/**
 * Aplica el tema guardado antes del primer paint para evitar el FOUC.
 * Lo ejecuta un script inline en <head>, no un efecto de React.
 */
export function themeInitScript(): string {
  return `(function(){try{var s=localStorage.getItem('${STORAGE_KEY}');var d=s?s==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;document.documentElement.classList.toggle('dark',d);}catch(e){}})();`;
}