import { EnvelopeIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';
import { clsx } from 'clsx';
import LanguageToggle from '@/components/ui/LanguageToggle';
import { type Lang, t } from '@/lib/i18n';

const GithubIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.612.069-.612 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.652.35-1.098.636-1.345-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.052 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
  </svg>
);

const LinkedInIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
    <path fillRule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.693 7 2.496v6.759z" clipRule="evenodd" />
  </svg>
);

const icons = {
  GitHub: <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.612.069-.612 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.652.35-1.098.636-1.345-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.052 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" /></svg>,
  LinkedIn: <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fillRule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.693 7 2.496v6.759z" clipRule="evenodd" /></svg>,
  Email: <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fillRule="evenodd" d="M3 4a2 2 0 012-2h14a2 2 0 012 2v16a2 2 0 01-2 2H5a2 2 0 01-2-2V4zm0 2v12h16V6H3zm8 5 7 5-7 5-7-5 7-5zm0 2-5 4 5 4 5-4-5-4z" /></svg>,
};

const socialLinks = [
  { name: 'GitHub', href: 'https://github.com/edu444477', icon: 'GitHub', ariaLabel: 'GitHub' },
  { name: 'LinkedIn', href: 'https://linkedin.com/in/edu444477', icon: 'LinkedIn', ariaLabel: 'LinkedIn' },
  { name: 'Email', href: 'mailto:eduardoorellanapomares@gmail.com', icon: 'Email', ariaLabel: 'Email' },
];

interface FooterProps {
  lang: 'es' | 'en';
}

export default function Footer({ lang }: FooterProps) {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark-50 dark:bg-dark-900 border-t border-dark-200 dark:border-dark-800" role="contentinfo">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-4">ED</h3>
            <p className="text-dark-600 dark:text-dark-400 text-sm leading-relaxed">
              Desarrollador Full Stack apasionado por crear aplicaciones web modernas, escalables y accesibles.
              Especializado en React, Python, bases de datos y arquitectura cloud.
            </p>
          </div>

          <nav aria-label="Enlaces rápidos">
            <h3 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-4">Enlaces</h3>
            <ul className="space-y-2">
              <li><a href="#inicio" className="text-sm text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Inicio</a></li>
              <li><a href="#experiencia" className="text-sm text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Experiencia</a></li>
              <li><a href="#proyectos" className="text-sm text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Proyectos</a></li>
              <li><a href="#tecnologias" className="text-sm text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Tecnologías</a></li>
              <li><a href="#contacto" className="text-sm text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Contacto</a></li>
            </ul>
          </nav>

          <div>
            <h3 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-4">Conectar</h3>
            <div className="flex gap-4">
              <a
                href="https://github.com/edu444477"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="GitHub"
                className="p-2 rounded-lg transition-all duration-200 text-dark-500 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-dark-100 dark:hover:bg-dark-800"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.612.069-.612 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.652.35-1.098.636-1.345-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.052 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" /></svg>
              </a>
              <a
                href="https://linkedin.com/in/edu444477"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="LinkedIn"
                className="p-2 rounded-lg transition-all duration-200 text-dark-500 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-dark-100 dark:hover:bg-dark-800"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fillRule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.693 7 2.496v6.759z" clipRule="evenodd" /></svg>
              </a>
              <a
                href="mailto:eduardoorellanapomares@gmail.com"
                aria-label="Email"
                className="p-2 rounded-lg transition-all duration-200 text-dark-500 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-dark-100 dark:hover:bg-dark-800"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fillRule="evenodd" d="M3 4a2 2 0 012-2h14a2 2 0 012 2v16a2 2 0 01-2 2H5a2 2 0 01-2-2V4zm0 2v12h16V6H3zm8 5 7 5-7 5-7-5 7-5zm0 2-5 4 5 4 5-4-5-4z" /></svg>
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-dark-200 dark:border-dark-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-dark-500 dark:text-dark-400">
              © {new Date().getFullYear()} ED. Construido con Astro, React, Tailwind CSS y mucho café.
            </p>
            <div className="flex items-center gap-4">
              <LanguageToggle lang={lang} />
              <div className="flex items-center gap-4 text-sm text-dark-500 dark:text-dark-400">
                <a href="#inicio" className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Volver arriba</a>
                <span aria-hidden="true">·</span>
                <a href={`/${lang}/privacidad`} className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Privacidad</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}