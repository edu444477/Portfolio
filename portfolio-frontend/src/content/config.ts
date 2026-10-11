import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    shortDescription: z.string(),
    techStack: z.array(z.string()),
    category: z.enum(['web', 'mobile', 'api', 'desktop', 'ai', 'other']),
    status: z.enum(['completed', 'in-progress', 'planned', 'archived']),
    featured: z.boolean().default(false),
    startDate: z.string().date(),
    endDate: z.string().date().optional(),
    repoUrl: z.string().url().optional(),
    liveUrl: z.string().url().optional(),
    image: z.string().optional(),
    images: z.array(z.string()).optional(),
    challenges: z.array(z.string()).optional(),
    learnings: z.array(z.string()).optional(),
    role: z.string().optional(),
    teamSize: z.number().optional(),
  }),
});

const experience = defineCollection({
  type: 'content',
  schema: z.object({
    role: z.string(),
    company: z.string(),
    location: z.string(),
    type: z.enum(['full-time', 'part-time', 'internship', 'freelance', 'education', 'project']),
    startDate: z.string().date(),
    endDate: z.string().date().optional(),
    current: z.boolean().default(false),
    description: z.string(),
    achievements: z.array(z.string()).optional(),
    techStack: z.array(z.string()),
    logo: z.string().optional(),
    website: z.string().url().optional(),
  }),
});

const tech = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    category: z.enum([
      'frontend',
      'backend',
      'database',
      'devops',
      'tools',
      'languages',
      'frameworks',
      'testing',
      'ai',
      'other',
    ]),
    level: z.enum(['expert', 'advanced', 'intermediate', 'beginner', 'learning']),
    years: z.number().optional(),
    icon: z.string().optional(),
    color: z.string().optional(),
    description: z.string().optional(),
    link: z.string().url().optional(),
    source: z.enum(['cv', 'tfg', 'portfolio']),
  }),
});

export const collections = { projects, experience, tech };