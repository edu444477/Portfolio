/**
 * Constantes del sitio - Identidad y configuración
 * RF-2: Todo el contenido dinámico desde contenido declarativo
 */

export const IDENTITY = {
  name: 'Eduardo Orellana',
  role: 'Desarrollador Full Stack',
  bio: 'Desarrollador Full Stack con más de 2 años de experiencia en el desarrollo de aplicaciones web y móviles para entornos empresariales. Especializado en React, React Native y Ruby on Rails, con experiencia en el diseño de APIs REST, desarrollo de interfaces modernas, aplicaciones multiplataforma y soluciones basadas en inteligencia artificial. Destaco por mi rápida adaptación a nuevos contextos técnicos, el aprendizaje continuo, la resolución de problemas y el compromiso con la calidad del software.',
  location: 'Marbella, Málaga, España',
  email: 'eduardoorellanapomares@gmail.com',
  phone: '+34 711 78 22 95',
  github: 'https://github.com/edu444477',
  linkedin: 'https://www.linkedin.com/in/eduardoorellanapomares/',
  availability: 'Abierto a oportunidades',
  skills: [
    'React',
    'React Native',
    'TypeScript',
    'Next.js',
    'Tailwind CSS',
    'Ruby on Rails',
    'PostgreSQL',
    'MySQL',
    'Git',
    'GitHub',
    'Jira',
    'Figma',
  ],
} as const;

export const SITE_CONFIG = {
  name: 'ED | Portfolio',
  url: 'https://portfolio-delta-eight-yx2zi6pmny.vercel.app',
  ogImage: '/og-default.png',
} as const;