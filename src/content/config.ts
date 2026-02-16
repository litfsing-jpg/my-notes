import { defineCollection, z } from 'astro:content';

const guides = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['seo', 'funnels', 'monetization', 'ai-tools']),
    categoryTitle: z.string(),
    module: z.number(),
    moduleTitle: z.string(),
    order: z.number(),
    icon: z.string().default('📄'),
  }),
});

export const collections = { guides };
