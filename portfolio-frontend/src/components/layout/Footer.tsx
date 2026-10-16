import { EnvelopeIcon } from '@heroicons/react/24/outline';
import LanguageToggle from '@/components/ui/LanguageToggle';
import { GithubIcon, LinkedInIcon } from '@/components/ui/BrandIcons';
import { IDENTITY } from '@/lib/constants';
import { t, localizePath, type Lang } from '@/lib/i18n';

const quickLinks = [
  { key: 'inicio', i18n: 'nav.inicio' },
  { key: 'experiencia', i18n: 'nav.experiencia' },
  { key: 'proyectos', i18n: 'nav.proyectos' },
  { key: 'tecnologias', i18n: 'nav.tecnologias' },
  { key: 'contacto', i18n: 'nav.contacto' },
] as const;

const socialLinks = [
  { key: 'github', i18n: 'footer.social.github', href: IDENTITY.github, icon: GithubIcon },
  { key: 'linkedin', i18n: 'footer.social.linkedin', href: IDENTITY.linkedin, icon: LinkedInIcon },
  { key: 'email', i18n: 'footer.social.email', href: `mailto:${IDENTITY.email}`, icon: EnvelopeIcon },
] as const;

interface FooterProps {
  lang: Lang;
  pathname: string;
}

export default function Footer({ lang, pathname }: FooterProps) {
  const homeHref = localizePath('/', lang);

  return (
    <footer className="bg-dark-50 dark:bg-dark-900 border-t border-dark-200 dark:border-dark-800" role="contentinfo">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h2 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-4">ED</h2>
            <p className="text-dark-600 dark:text-dark-400 text-sm leading-relaxed">
              {t('footer.bio', lang)}
            </p>
          </div>

          <nav aria-label={t('footer.quickLinks', lang)}>
            <h2 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-4">{t('footer.links', lang)}</h2>
            <ul className="space-y-2">
              {quickLinks.map((item) => (
                <li key={item.key}>
                  <a
                    href={`${homeHref}#${item.key}`}
                    className="text-sm text-dark-600 dark:text-dark-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                  >
                    {t(item.i18n, lang)}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          <div>
            <h2 className="text-lg font-semibold text-dark-900 dark:text-dark-100 mb-4">{t('footer.connect', lang)}</h2>
            <div className="flex gap-4">
              {socialLinks.map((link) => {
                const Icon = link.icon;
                const external = link.key !== 'email';
                return (
                  <a
                    key={link.key}
                    href={link.href}
                    {...(external ? { target: '_blank', rel: 'noopener noreferrer' } : {})}
                    aria-label={t(link.i18n, lang)}
                    className="p-2 rounded-lg transition-all duration-200 text-dark-500 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-dark-100 dark:hover:bg-dark-800 focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2 dark:focus:ring-offset-dark-900"
                  >
                    <Icon className="w-5 h-5" aria-hidden="true" />
                  </a>
                );
              })}
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-dark-200 dark:border-dark-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-dark-500 dark:text-dark-400">
              {t('footer.rights', lang, { year: String(new Date().getFullYear()) })}
            </p>
            <div className="flex items-center gap-4">
              <LanguageToggle lang={lang} pathname={pathname} />
              <div className="flex items-center gap-4 text-sm text-dark-500 dark:text-dark-400">
                <a href={`${homeHref}#inicio`} className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                  {t('footer.backToTop', lang)}
                </a>
                <span aria-hidden="true">·</span>
                <a
                  href={localizePath('/privacidad', lang)}
                  className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                >
                  {t('footer.privacy', lang)}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}