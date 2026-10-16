import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import vercel from '@astrojs/vercel';
import path from 'path';

export default defineConfig({
  site: 'https://portfolio-delta-eight-yx2zi6pmny.vercel.app',
  integrations: [
    react(),
    tailwind(),
    mdx(),
    sitemap(),
  ],
  // Adapter (no integration): genera la función serverless /api/contact.
  adapter: vercel(),
  // 'server' solo para poder generar la función /api/contact (la clave de
  // Web3Forms no puede ir en el bundle del cliente). Todas las páginas de
  // contenido llevan `export const prerender = true`, así que siguen
  // sirviéndose como HTML estático desde el CDN.
  output: 'server',
  trailingSlash: 'always',
  build: {
    inlineStylesheets: 'auto',
  },
  i18n: {
    defaultLocale: 'es',
    locales: ['es', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  vite: {
    resolve: {
      alias: {
        '@': path.resolve('./src'),
        '@components': path.resolve('./src/components'),
        '@layouts': path.resolve('./src/layouts'),
        '@pages': path.resolve('./src/pages'),
        '@styles': path.resolve('./src/styles'),
        '@lib': path.resolve('./src/lib'),
        '@content': path.resolve('./src/content'),
      },
    },
    optimizeDeps: {
      include: ['@heroicons/react/24/outline', '@heroicons/react/24/solid'],
    },
  },
});