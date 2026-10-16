/**
 * Constantes del sitio - Identidad y configuración
 * RF-2: Todo el contenido dinámico desde contenido declarativo
 *
 * Los campos visibles van en ES y EN (RFN-2). Los neutrales (email, enlaces)
 * son un único valor. `story` alimenta la sección About con párrafos reales
 * en vez de repetir la bio.
 */

import type { Lang } from '@/lib/i18n';

export const IDENTITY = {
  name: 'Eduardo Orellana',
  role: {
    es: 'Desarrollador Full Stack',
    en: 'Full Stack Developer',
  },
  bio: {
    es: 'Desarrollador Full Stack con más de 2 años de experiencia en el desarrollo de aplicaciones web y móviles para entornos empresariales. Especializado en React, React Native y Ruby on Rails, con experiencia en el diseño de APIs REST, desarrollo de interfaces modernas, aplicaciones multiplataforma y soluciones basadas en inteligencia artificial. Destaco por mi rápida adaptación a nuevos contextos técnicos, el aprendizaje continuo, la resolución de problemas y el compromiso con la calidad del software.',
    en: 'Full Stack Developer with over 2 years of experience building web and mobile applications for enterprise environments. Specialized in React, React Native, and Ruby on Rails, with experience designing REST APIs, developing modern interfaces, cross-platform applications, and AI-based solutions. I stand out for my quick adaptation to new technical contexts, continuous learning, problem solving, and commitment to software quality.',
  },
  // Párrafos de la sección About ("Mi historia"). Contenido, no interfaz.
  story: {
    es: [
      'Desarrollador Full Stack con formación en Ingeniería Informática y especialización en arquitectura de software moderno. Mi trayectoria combina desarrollo frontend con React/TypeScript, backend con Python (Flask/FastAPI), bases de datos relacionales y DevOps.',
      'Mi Trabajo de Fin de Grado "La Nueva Era" es una plataforma completa de e-commerce para videojuegos de segunda mano con panel de administración RRHH, demostrando capacidad para entregar proyectos end-to-end: desde requisitos hasta despliegue en producción.',
      'Actualmente profundizando en ingeniería con IA (SDD, multi-agentes, skills, MCP) para elevar la calidad y velocidad de desarrollo, aplicando metodologías que usan equipos de alto rendimiento en empresas tecnológicas punteras.',
    ],
    en: [
      'Full Stack Developer with a degree in Computer Engineering and a specialization in modern software architecture. My track record combines frontend development with React/TypeScript, backend work with Python (Flask/FastAPI), relational databases, and DevOps.',
      'My final degree project "La Nueva Era" is a complete second-hand video game e-commerce platform with an HR administration panel, demonstrating the ability to deliver end-to-end projects: from requirements through production deployment.',
      'Currently going deeper into AI engineering (SDD, multi-agents, skills, MCP) to raise development quality and speed, applying the methodologies used by high-performing teams at leading tech companies.',
    ],
  },
  location: {
    es: 'Marbella, Málaga, España',
    en: 'Marbella, Málaga, Spain',
  },
  availability: {
    es: 'Abierto a oportunidades',
    en: 'Open to opportunities',
  },
  email: 'eduardoorellanapomares@gmail.com',
  phone: '+34 711 78 22 95',
  github: 'https://github.com/edu444477',
  linkedin: 'https://www.linkedin.com/in/eduardoorellanapomares/',
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

/** Resuelve un campo bilingüe de IDENTITY para el idioma activo. */
export function localize(value: { es: string; en: string }, lang: Lang): string {
  return value[lang] ?? value.es;
}

export const SITE_CONFIG = {
  name: 'ED | Portfolio',
  url: 'https://portfolio-delta-eight-yx2zi6pmny.vercel.app',
  ogImage: '/og-default.png',
} as const;