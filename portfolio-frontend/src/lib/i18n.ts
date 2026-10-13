/**
 * Internacionalización (i18n) - Diccionarios y helpers
 * RF-8, RF-11, RF-12, RF-13, RFN-2, RFN-8
 */

export type Lang = 'es' | 'en';

export type Dict = Record<string, string>;

export const dicts: Record<Lang, Dict> = {
  es: {
    // Navegación
    'nav.inicio': 'Inicio',
    'nav.experiencia': 'Experiencia',
    'nav.proyectos': 'Proyectos',
    'nav.tecnologias': 'Tecnologías',
    'nav.contacto': 'Contacto',

    // Hero
    'hero.title': 'Hola, soy',
    'hero.role': 'Desarrollador Full Stack',
    'hero.description': 'Desarrollador Full Stack con más de 2 años de experiencia en el desarrollo de aplicaciones web y móviles para entornos empresariales. Especializado en React, React Native y Ruby on Rails, con experiencia en el diseño de APIs REST, desarrollo de interfaces modernas, aplicaciones multiplataforma y soluciones basadas en inteligencia artificial. Destaco por mi rápida adaptación a nuevos contextos técnicos, el aprendizaje continuo, la resolución de problemas y el compromiso con la calidad del software.',
    'hero.cta.projects': 'Ver proyectos',
    'hero.cta.contact': 'Contactar',

    // About
    'about.myStory': 'Mi historia',
    'about.profile': 'Perfil',
    'about.name': 'Nombre',
    'about.role': 'Rol',
    'about.location': 'Ubicación',
    'about.availability': 'Disponibilidad',
    'about.email': 'Email',
    'about.skills': 'Habilidades destacadas',

    // Experience
    'experience.title': 'Experiencia profesional',
    'experience.education': 'Formación',
    'experience.current': 'Actualidad',
    'experience.techStack': 'Tecnologías',

    // Projects
    'projects.title': 'Proyectos destacados',
    'projects.other': 'Otros proyectos',
    'projects.viewDetail': 'Ver detalle',
    'projects.code': 'Código',
    'projects.demo': 'Demo',
    'projects.status.completed': 'Completado',
    'projects.status.in-progress': 'En progreso',
    'projects.status.planned': 'Planificado',
    'projects.status.archived': 'Archivado',
    'projects.challenges': 'Retos principales',
    'projects.learnings': 'Aprendizajes',
    'projects.techStack': 'Stack técnico',

    // Tech Stack
    'tech.title': 'Stack tecnológico',
    'tech.years': 'año',
    'tech.years_plural': 'años',
    'tech.level.expert': 'Experto',
    'tech.level.advanced': 'Avanzado',
    'tech.level.intermediate': 'Intermedio',
    'tech.level.beginner': 'Principiante',
    'tech.level.learning': 'Aprendiendo',
    'tech.docs': 'Docs',
    'tech.source.cv': 'CV',
    'tech.source.tfg': 'TFG',
    'tech.source.portfolio': 'Portfolio',

    // Contact
    'contact.title': 'Contacta conmigo',
    'contact.subtitle': '¿Tienes un proyecto en mente? ¿Quieres colaborar? ¿Solo saludar? Escríbeme.',
    'contact.info.title': 'Información de contacto',
    'contact.info.email': 'Email',
    'contact.info.github': 'GitHub',
    'contact.info.linkedin': 'LinkedIn',
    'contact.info.location': 'Ubicación',
    'contact.info.availability': 'Disponibilidad',
    'contact.form.title': 'Enviar mensaje',
    'contact.form.name': 'Nombre',
    'contact.form.email': 'Email',
    'contact.form.subject': 'Asunto',
    'contact.form.message': 'Mensaje',
    'contact.form.submit': 'Enviar mensaje',
    'contact.form.submitting': 'Enviando...',
    'contact.form.success': '¡Mensaje enviado! Te responderé pronto.',
    'contact.form.error': 'Error al enviar. Intenta de nuevo o escríbeme directamente a {email}',
    'contact.form.error.required': 'Este campo es obligatorio',
    'contact.form.error.email': 'Formato de email inválido',
    'contact.form.privacy': 'Al enviar, aceptas la <a href="/privacy">política de privacidad</a>. Respondo en 24-48h laborables.',

    // Footer
    'footer.rights': '© {year} ED. Construido con Astro, React, Tailwind CSS y mucho café.',
    'footer.backToTop': 'Volver arriba',
    'footer.privacy': 'Privacidad',

    // Theme
    'theme.toDark': 'Cambiar a modo oscuro',
    'theme.toLight': 'Cambiar a modo claro',

    // Language
    'lang.switchTo': 'Cambiar a {lang}',
    'lang.es': 'ES',
    'lang.en': 'EN',

    // Privacy
    'privacy.title': 'Política de privacidad',
    'privacy.intro': 'Esta política explica cómo se tratan los datos personales al usar este sitio web y el formulario de contacto.',
    'privacy.dataController': 'Responsable del tratamiento',
    'privacy.dataControllerValue': 'Eduardo Orellana Pomares (eduardoorellanapomares@gmail.com)',
    'privacy.purpose': 'Finalidad',
    'privacy.purposeValue': 'Gestionar los mensajes enviados a través del formulario de contacto y responder a las consultas.',
    'privacy.legalBasis': 'Legitimación',
    'privacy.legalBasisValue': 'Consentimiento del interesado al enviar el formulario.',
    'privacy.recipients': 'Destinatarios',
    'privacy.recipientsValue': 'Los datos se envían a Web3Forms (servicio de gestión de formularios) y no se ceden a terceros salvo obligación legal.',
    'privacy.rights': 'Derechos',
    'privacy.rightsValue': 'Acceso, rectificación, supresión, limitación, portabilidad y oposición. Puedes ejercerlos escribiendo a eduardoorellanapomares@gmail.com.',
    'privacy.web3forms': 'Uso de Web3Forms',
    'privacy.web3formsValue': 'El formulario usa Web3Forms para el envío. La clave pública de Web3Forms se incluye en el código del lado del cliente por diseño del servicio. No se almacenan datos personales en este sitio web más allá del envío del formulario.',

    // 404
    'notfound.title': 'Página no encontrada',
    'notfound.message': 'Lo sentimos, la página que buscas no existe o ha sido movida.',
    'notfound.home': 'Volver al inicio',
    'notfound.projects': 'Ver proyectos',

    // Skip link
    'skip.main': 'Saltar al contenido principal',
  },
  en: {
    // Navigation
    'nav.inicio': 'Home',
    'nav.experiencia': 'Experience',
    'nav.proyectos': 'Projects',
    'nav.tecnologias': 'Tech Stack',
    'nav.contacto': 'Contact',

    // Hero
    'hero.title': 'Hi, I\'m',
    'hero.role': 'Full Stack Developer',
    'hero.description': 'Full Stack Developer with over 2 years of experience building web and mobile applications for enterprise environments. Specialized in React, React Native, and Ruby on Rails, with experience designing REST APIs, developing modern interfaces, cross-platform applications, and AI-based solutions. I stand out for my quick adaptation to new technical contexts, continuous learning, problem solving, and commitment to software quality.',
    'hero.cta.projects': 'View projects',
    'hero.cta.contact': 'Contact',

    // About
    'about.myStory': 'My story',
    'about.profile': 'Profile',
    'about.name': 'Name',
    'about.role': 'Role',
    'about.location': 'Location',
    'about.availability': 'Availability',
    'about.email': 'Email',
    'about.skills': 'Featured skills',

    // Experience
    'experience.title': 'Professional Experience',
    'experience.education': 'Education',
    'experience.current': 'Present',
    'experience.techStack': 'Technologies',

    // Projects
    'projects.title': 'Featured Projects',
    'projects.other': 'Other Projects',
    'projects.viewDetail': 'View detail',
    'projects.code': 'Code',
    'projects.demo': 'Demo',
    'projects.status.completed': 'Completed',
    'projects.status.in-progress': 'In progress',
    'projects.status.planned': 'Planned',
    'projects.status.archived': 'Archived',
    'projects.challenges': 'Main challenges',
    'projects.learnings': 'Learnings',
    'projects.techStack': 'Tech stack',

    // Tech Stack
    'tech.title': 'Tech Stack',
    'tech.years': 'year',
    'tech.years_plural': 'years',
    'tech.level.expert': 'Expert',
    'tech.level.advanced': 'Advanced',
    'tech.level.intermediate': 'Intermediate',
    'tech.level.beginner': 'Beginner',
    'tech.level.learning': 'Learning',
    'tech.docs': 'Docs',
    'tech.source.cv': 'CV',
    'tech.source.tfg': 'TFG',
    'tech.source.portfolio': 'Portfolio',

    // Contact
    'contact.title': 'Get in touch',
    'contact.subtitle': 'Have a project in mind? Want to collaborate? Just want to say hi? Write to me.',
    'contact.info.title': 'Contact information',
    'contact.info.email': 'Email',
    'contact.info.github': 'GitHub',
    'contact.info.linkedin': 'LinkedIn',
    'contact.info.location': 'Location',
    'contact.info.availability': 'Availability',
    'contact.form.title': 'Send message',
    'contact.form.name': 'Name',
    'contact.form.email': 'Email',
    'contact.form.subject': 'Subject',
    'contact.form.message': 'Message',
    'contact.form.submit': 'Send message',
    'contact.form.submitting': 'Sending...',
    'contact.form.success': 'Message sent! I\'ll get back to you soon.',
    'contact.form.error': 'Failed to send. Try again or write directly to {email}',
    'contact.form.error.required': 'This field is required',
    'contact.form.error.email': 'Invalid email format',
    'contact.form.privacy': 'By sending, you accept the <a href="/privacy">privacy policy</a>. I reply within 24-48h on business days.',

    // Footer
    'footer.rights': '© {year} ED. Built with Astro, React, Tailwind CSS and lots of coffee.',
    'footer.backToTop': 'Back to top',
    'footer.privacy': 'Privacy',

    // Theme
    'theme.toDark': 'Switch to dark mode',
    'theme.toLight': 'Switch to light mode',

    // Language
    'lang.switchTo': 'Switch to {lang}',
    'lang.es': 'ES',
    'lang.en': 'EN',

    // Privacy
    'privacy.title': 'Privacy Policy',
    'privacy.intro': 'This policy explains how personal data is processed when using this website and the contact form.',
    'privacy.dataController': 'Data Controller',
    'privacy.dataControllerValue': 'Eduardo Orellana Pomares (eduardoorellanapomares@gmail.com)',
    'privacy.purpose': 'Purpose',
    'privacy.purposeValue': 'Manage messages sent through the contact form and respond to inquiries.',
    'privacy.legalBasis': 'Legal Basis',
    'privacy.legalBasisValue': 'Consent of the data subject when submitting the form.',
    'privacy.recipients': 'Recipients',
    'privacy.recipientsValue': 'Data is sent to Web3Forms (form management service) and is not shared with third parties except by legal obligation.',
    'privacy.rights': 'Rights',
    'privacy.rightsValue': 'Access, rectification, erasure, restriction, portability, and objection. Exercise them by writing to eduardoorellanapomares@gmail.com.',
    'privacy.web3forms': 'Web3Forms Usage',
    'privacy.web3formsValue': 'The form uses Web3Forms for submission. The Web3Forms public key is included in client-side code by service design. No personal data is stored on this website beyond form submission.',

    // 404
    'notfound.title': 'Page not found',
    'notfound.message': 'Sorry, the page you\'re looking for doesn\'t exist or has been moved.',
    'notfound.home': 'Back to home',
    'notfound.projects': 'View projects',

    // Skip link
    'skip.main': 'Skip to main content',
  },
};

export function t(key: string, lang: Lang, params?: Record<string, string>): string {
  let str = dicts[lang][key] || dicts.es[key] || key;
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      str = str.replace(new RegExp(`\\{${k}\\}`, 'g'), v);
    });
  }
  return str;
}

export function getSlug(key: string, lang: Lang): string {
  const slugs: Record<string, Record<Lang, string>> = {
    inicio: { es: 'inicio', en: 'home' },
    experiencia: { es: 'experiencia', en: 'experience' },
    proyectos: { es: 'proyectos', en: 'projects' },
    tecnologias: { es: 'tecnologias', en: 'tech-stack' },
    contacto: { es: 'contacto', en: 'contact' },
    privacidad: { es: 'privacidad', en: 'privacy' },
  };
  return slugs[key]?.[lang] || key;
}

export function getLangFromUrl(url: URL): Lang {
  const segments = url.pathname.split('/').filter(Boolean);
  const first = segments[0];
  if (first === 'es' || first === 'en') return first;
  return 'es';
}

export function getAlternateUrls(pathname: string): { es: string; en: string; xDefault: string } {
  const base = 'https://portfolio-delta-eight-yx2zi6pmny.vercel.app';
  const cleanPath = pathname.replace(/^\/(es|en)/, '') || '/';
  return {
    es: `${base}/es${cleanPath}`,
    en: `${base}/en${cleanPath}`,
    xDefault: `${base}/es${cleanPath}`,
  };
}