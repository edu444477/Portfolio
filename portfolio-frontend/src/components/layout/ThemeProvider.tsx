import { useSyncExternalStore } from 'react';
import { getSnapshot, setTheme as setThemeStore, subscribe, toggleTheme as toggleThemeStore, type Theme } from '@/lib/theme';

/**
 * Hook del tema (RF-28, RF-29).
 *
 * No hay contexto a propósito: Astro renderiza `Header` y `Footer` como HTML
 * del servidor fuera del árbol de React, así que un Provider no los alcanza.
 * Un island lee el store exterior directamente con useSyncExternalStore, que
 * además da el mismo snapshot en servidor y cliente (sin hydration mismatch).
 */
export function useTheme() {
  const theme = useSyncExternalStore(subscribe, getSnapshot, () => 'light');

  return {
    theme,
    toggleTheme: () => toggleThemeStore(),
    setTheme: (newTheme: Theme) => setThemeStore(newTheme),
  };
}