
export interface SpecialistAgent {
    id: string;
    name: string;
    description: string;
    icon: string;
    details: string[];
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
    type: string;
    accent: string;
}

export const SPECIALIST_AGENTS: SpecialistAgent[] = [
    {
        id: '1',
        name: 'NIST Controls',
        description: '800-53 Rev.5 & RMF expertise',
        icon: 'shield',
        details: [
            'Automated constraint verification against 800-53 baselines.',
            'Real-time RMF mapping for selected controls.',
            'Instant parameter resolution for assignment statements.'
        ]
    },
    {
        id: '2',
        name: 'Audit & Assessment',
        description: 'Evidence & test procedures',
        icon: 'clipboard',
        details: [
            'Auto-generation of assessable test procedures (53A).',
            'Evidence artifact correlation with specific control mandates.',
            'Mock audit simulation for readiness checks.'
        ]
    },
    {
        id: '3',
        name: 'Risk & Impact',
        description: 'FIPS 199 & CIA analysis',
        icon: 'alert',
        details: [
            'Dynamic FIPS 199 security categorization.',
            'CIA triad impact analysis for system components.',
            'Risk exposure calculation based on control tailoring.'
        ]
    },
    {
        id: '4',
        name: 'Compliance Mapping',
        description: 'FedRAMP, CMMC, ISO',
        icon: 'map',
        details: [
            'Cross-framework harmonization (FedRAMP <-> 800-53).',
            'Gap analysis automation for multi-standard compliance.',
            'Inheritance model visualization for cloud consumers.'
        ]
    },
    {
        id: '5',
        name: 'Product Manager',
        description: 'Roadmaps & prioritization',
        icon: 'target',
        details: [
            'Feature prioritization based on compliance debt.',
            'Roadmap alignment with ATO milestones.',
            'Stakeholder communication templates for security blockers.'
        ]
    },
    {
        id: '6',
        name: 'QA & Test Strategy',
        description: 'Test cases & validation',
        icon: 'check-circle',
        details: [
            'Automated test case generation aligned with SP 800-53A.',
            'Control validation criteria and coverage matrices.',
            'Regression and acceptance testing for security controls.'
        ]
    },
    {
        id: '7',
        name: 'DevSecOps',
        description: 'CI/CD & pipeline security',
        icon: 'terminal',
        details: [
            'CI/CD pipeline hardening with SAST/DAST integration.',
            'Container and infrastructure-as-code security scanning.',
            'Shift-left compliance automation and dependency analysis.'
        ]
    },
];

export const KNOWLEDGE_BASE: KnowledgeItem[] = [
    { id: 'kb1', title: 'NIST SP 800-53 Rev.5', link: 'https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final' },
    { id: 'kb2', title: 'NIST SP 1362', link: 'https://csrc.nist.gov/publications/' }, // specific URL unclear, linking to pubs
    { id: 'kb3', title: 'FedRAMP Guidelines', link: 'https://www.fedramp.gov/documents-templates/' },
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
