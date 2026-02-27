
export interface SpecialistAgent {
  id: string;
  name: string;
  description: string;
  icon: string;
}

export interface KnowledgeItem {
  id: string;
  title: string;
  link: string;
}

export interface BentoMetadata {
  id: string;
  title: string;
  content: string;
  type: 'pain-point' | 'design-thinking' | 'empathize';
  accent: string;
}

// Added FeaturedProject interface for Portfolio highlights
export interface FeaturedProject {
  id: string;
  title: string;
  link: string;
  imageUrl: string;
}

// Added PortfolioItem interface for thought leadership cards
export interface PortfolioItem {
  id: number;
  title: string;
  description: string;
  buttonText: string;
  buttonLink: string;
  isDark?: boolean;
}
