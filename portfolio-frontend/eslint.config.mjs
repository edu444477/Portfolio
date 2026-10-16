import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import astro from 'eslint-plugin-astro';
import reactHooks from 'eslint-plugin-react-hooks';

export default tseslint.config(
  {
    ignores: ['dist/**', '.vercel/**', 'node_modules/**', '.astro/**', 'src/content/**'],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...astro.configs.recommended,
  {
    files: ['**/*.{ts,tsx,astro}'],
    plugins: { 'react-hooks': reactHooks },
    rules: {
      ...reactHooks.configs.recommended.rules,
      // Las props de los islands se decluran con interfaces: bien tipado, no hace falta prop-types.
      'react-hooks/rules-of-hooks': 'error',
    },
  },
  {
    // Content Collections y ficheros de config: no son código de app.
    files: ['src/content/config.ts', 'astro.config.mjs', 'tailwind.config.mjs'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
);