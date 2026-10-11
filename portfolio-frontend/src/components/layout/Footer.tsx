import { GithubIcon, LinkedInIcon, MailIcon, ExternalLinkIcon } from '@heroicons/react/24/outline';
import { clsx } from 'clsx';

const socialLinks = [
  { name: 'GitHub', href: 'https://github.com/edu444477', icon: GithubIcon, ariaLabel: 'GitHub' },
  { name: 'LinkedIn', href: 'https://linkedin.com/in/edu444477', icon: LinkedInIcon, ariaLabel: 'LinkedIn' },
  { name: 'Email', href: 'mailto:edu@example.com', icon: MailIcon, ariaLabel: 'Email' },
];

export function Footer() {
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
              {socialLinks.map((social) => (
                <a
                  key={social.name}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={social.ariaLabel}
                  className={clsx(
                    'p-2 rounded-lg transition-all duration-200',
                    'text-dark-500 hover:text-primary-600 dark:hover:text-primary-400',
                    'hover:bg-dark-100 dark:hover:bg-dark-800'
                  )}
                >
                  <social.icon className="w-5 h-5" aria-hidden="true" />
                </a>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-dark-200 dark:border-dark-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-dark-500 dark:text-dark-400">
              © {currentYear} ED. Construido con Astro, React, Tailwind CSS y mucho café.
            </p>
            <div className="flex items-center gap-4 text-sm text-dark-500 dark:text-dark-400">
              <a href="#inicio" className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Volver arriba</a>
              <span aria-hidden="true">·</span>
              <a href="/privacy" className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Privacidad</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}