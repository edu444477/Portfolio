import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://portfolio-delta-eight-yx2zi6pmny.vercel.app',
  integrations: [
    react(),
    tailwind(),
    mdx(),
    sitemap(),
  ],
  output: 'static',
  trailingSlash: 'always',
  build: {
    inlineStylesheets: 'auto',
  },
  vite: {
    optimizeDeps: {
      include: ['@heroicons/react/24/outline', '@heroicons/react/24/solid'],
    },
  },
});