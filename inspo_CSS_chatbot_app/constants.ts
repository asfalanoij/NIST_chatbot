
import { SpecialistAgent, KnowledgeItem, BentoMetadata, FeaturedProject, PortfolioItem } from './types';

export const SPECIALIST_AGENTS: SpecialistAgent[] = [
  { id: '1', name: 'NIST Controls', description: '800-53 Rev.5 & RMF expertise', icon: 'shield' },
  { id: '2', name: 'Audit & Assessment', description: 'Evidence & test procedures', icon: 'clipboard' },
  { id: '3', name: 'Risk & Impact', description: 'FIPS 199 & CIA analysis', icon: 'alert' },
  { id: '4', name: 'Compliance Mapping', description: 'FedRAMP, CMMC, ISO', icon: 'map' },
  { id: '5', name: 'Product Manager', description: 'Roadmaps & prioritization', icon: 'target' },
];

export const KNOWLEDGE_BASE: KnowledgeItem[] = [
  { id: 'kb1', title: 'NIST SP 800-53 Rev.5', link: '#' },
  { id: 'kb2', title: 'NIST SP 1362', link: '#' },
  { id: 'kb3', title: 'FedRAMP Guidelines', link: '#' },
];

export const BENTO_METADATA: BentoMetadata[] = [
  {
    id: 'b1',
    title: 'Pain Points',
    content: 'Navigating 1000+ controls without context leads to compliance fatigue and security gaps.',
    type: 'pain-point',
    accent: '#5D5CDE'
  },
  {
    id: 'b2',
    title: 'Design Thinking',
    content: 'Context-aware RAG allows for real-time mapping of technical evidence to regulatory requirements.',
    type: 'design-thinking',
    accent: '#4AB7C3'
  },
  {
    id: 'b3',
    title: 'Empathize',
    content: 'Auditors need clarity, not just data. We prioritize actionable insights over static documentation.',
    type: 'empathize',
    accent: '#FFFFFF'
  }
];

// Added FEATURED_PROJECTS to support FeaturedSection.tsx
export const FEATURED_PROJECTS: FeaturedProject[] = [
  {
    id: 'f1',
    title: 'Cloud Security Audit for Financial Sector',
    link: '#',
    imageUrl: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=1200'
  },
  {
    id: 'f2',
    title: 'NIST 800-53 Compliance Modernization',
    link: '#',
    imageUrl: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=800'
  },
  {
    id: 'f3',
    title: 'Federal Risk Management Framework',
    link: '#',
    imageUrl: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc51?auto=format&fit=crop&q=80&w=800'
  }
];

// Added PORTFOLIO_ITEMS to support PortfolioSection.tsx
export const PORTFOLIO_ITEMS: PortfolioItem[] = [
  {
    id: 1,
    title: 'Audit Automation',
    description: 'Scaling security oversight through automated evidence collection and validation.',
    buttonText: 'View Case Study',
    buttonLink: '#',
    isDark: true
  },
  {
    id: 2,
    title: 'GRC Strategy',
    description: 'Developing resilient governance structures for high-stakes digital assets.',
    buttonText: 'Explore Strategy',
    buttonLink: '#'
  },
  {
    id: 3,
    title: 'Cyber Education',
    description: 'Bridging the gap between technical security and executive decision-making.',
    buttonText: 'Learn More',
    buttonLink: '#'
  }
];
