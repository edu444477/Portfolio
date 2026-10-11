import { ArrowDownTrayIcon, ComputerDesktopIcon, CodeBracketIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { clsx } from 'clsx';

interface HeroProps {
  name: string;
  title: string;
  description: string;
  ctaText?: string;
  ctaHref?: string;
  secondaryCtaText?: string;
  secondaryCtaHref?: string;
}

export function Hero({ name, title, description, ctaText = 'Ver proyectos', ctaHref = '#proyectos', secondaryCtaText = 'Contactar', secondaryCtaHref = '#contacto' }: HeroProps) {
  return (
    <section id="inicio" className="relative min-h-screen flex items-center justify-center pt-16 px-4 sm:px-6 lg:px-8 overflow-hidden" aria-labelledby="hero-title">
      <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-dark-50 dark:from-dark-900 dark:via-dark-950 dark:to-dark-900" aria-hidden="true" />
      <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center bg-auto opacity-5 dark:opacity-10" aria-hidden="true" />
      
      <div className="relative mx-auto max-w-7xl">
        <div className="text-center max-w-3xl mx-auto animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6 animate-slide-up">
            <SparklesIcon className="w-4 h-4" aria-hidden="true" />
            <span>Desarrollador Full Stack</span>
          </div>

          <h1 id="hero-title" className="text-4xl sm:text-5xl lg:text-6xl font-bold text-dark-900 dark:text-dark-100 mb-6 animate-slide-up" style={{ animationDelay: '100ms' }}>
            Hola, soy <span className="text-primary-600 dark:text-primary-400">{name}</span>
          </h1>

          <h2 className="text-xl sm:text-2xl lg:text-3xl text-dark-600 dark:text-dark-300 mb-6 font-medium animate-slide-up" style={{ animationDelay: '200ms' }}>
            {title}
          </h2>

          <p className="text-lg sm:text-xl text-dark-600 dark:text-dark-400 mb-10 max-w-2xl mx-auto leading-relaxed animate-slide-up" style={{ animationDelay: '300ms' }}>
            {description}
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up" style={{ animationDelay: '400ms' }}>
            <a
              href={ctaHref}
              className={clsx(
                'inline-flex items-center gap-2 px-8 py-3.5 rounded-lg font-semibold text-base',
                'bg-primary-600 text-white hover:bg-primary-700',
                'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900',
                'transition-all duration-200 shadow-lg shadow-primary-500/25'
              )}
            >
              {ctaText}
              <ArrowDownTrayIcon className="w-5 h-5" aria-hidden="true" />
            </a>
            <a
              href={secondaryCtaHref}
              className={clsx(
                'inline-flex items-center gap-2 px-8 py-3.5 rounded-lg font-semibold text-base',
                'border-2 border-dark-300 dark:border-dark-600 text-dark-700 dark:text-dark-300',
                'hover:bg-dark-100 dark:hover:bg-dark-800',
                'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900',
                'transition-all duration-200'
              )}
            >
              {secondaryCtaText}
              <ExternalLinkIcon className="w-5 h-5" aria-hidden="true" />
            </a>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 animate-fade-in" style={{ animationDelay: '500ms' }}>
          <div className="text-center p-6 rounded-xl bg-white/50 dark:bg-dark-800/50 backdrop-blur-sm border border-dark-200 dark:border-dark-700">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 mb-4 mx-auto">
              <CodeBracketIcon className="w-7 h-7" aria-hidden="true" />
            </div>
            <h3 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-2">Código Limpio</h3>
            <p className="text-dark-600 dark:text-dark-400 text-sm">Arquitectura mantenible, tipado estricto y pruebas automatizadas</p>
          </div>
          <div className="text-center p-6 rounded-xl bg-white/50 dark:bg-dark-800/50 backdrop-blur-sm border border-dark-200 dark:border-dark-700">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 mb-4 mx-auto">
              <ComputerDesktopIcon className="w-7 h-7" aria-hidden="true" />
            </div>
            <h3 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-2">Rendimiento</h3>
            <p className="text-dark-600 dark:text-dark-400 text-sm">Lighthouse 100/100, Core Web Vitals optimizados, carga instantánea</p>
          </div>
          <div className="text-center p-6 rounded-xl bg-white/50 dark:bg-dark-800/50 backdrop-blur-sm border border-dark-200 dark:border-dark-700">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 mb-4 mx-auto">
              <SparklesIcon className="w-7 h-7" aria-hidden="true" />
            </div>
            <h3 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-2">Accesibilidad</h3>
            <p className="text-dark-600 dark:text-dark-400 text-sm">WCAG 2.1 AA, semántica HTML, navegación por teclado, screen readers</p>
          </div>
        </div>
      </div>

      <a
        href="#experiencia"
        className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce"
        aria-label="Desplazarse a experiencia"
      >
        <ArrowDownTrayIcon className="w-6 h-6 text-dark-400 dark:text-dark-600" aria-hidden="true" />
      </a>
    </section>
  );
}