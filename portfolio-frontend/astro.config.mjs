import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import path from 'path';

export default defineConfig({
  site: 'https://portfolio-delta-eight-yx2zi6pmny.vercel.app',
  integrations: [
    react(),
    tailwind(),
    mdx(),
    sitemap(),
  ],
  // 100% estático. El formulario de contacto envía directo a Web3Forms desde
  // el navegador: su API rechaza las llamadas que llegan desde un servidor
  // (403 "method not allowed"), así que no sirve un endpoint propio.
  output: 'static',
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