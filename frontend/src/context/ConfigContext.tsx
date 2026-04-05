import React, { createContext, useContext, useState, useEffect } from 'react';
import { API_BASE } from '../config';

export interface SpecialistAgent {
    id: string;
    name: string;
    description: string;
    icon: string;
    details: string[];
}

export interface CrossmapEntry {
    nist_id: string;
    nist_title: string;
    nist_family: string;
    iso27001: string[];
    iso27001_titles: string[];
    csf2: string[];
    csf2_titles: string[];
    iso27005: string[];
    iso27005_titles: string[];
}

interface ConfigContextType {
    agents: SpecialistAgent[];
    crossmap: CrossmapEntry[];
    loading: boolean;
    error: string | null;
}

const ConfigContext = createContext<ConfigContextType | undefined>(undefined);

export const ConfigProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [agents, setAgents] = useState<SpecialistAgent[]>([]);
    const [crossmap, setCrossmap] = useState<CrossmapEntry[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const [agentsRes, crossmapRes] = await Promise.all([
                    fetch(`${API_BASE}/api/config/agents`),
                    fetch(`${API_BASE}/api/config/crossmap`)
                ]);

                if (!agentsRes.ok || !crossmapRes.ok) {
                    throw new Error('Failed to fetch configuration');
                }

                const [agentsData, crossmapData] = await Promise.all([
                    agentsRes.json(),
                    crossmapRes.json()
                ]);

                setAgents(agentsData);
                setCrossmap(crossmapData);
            } catch (err) {
                console.error('Error fetching config:', err);
                setError(err instanceof Error ? err.message : 'Unknown error');
            } finally {
                setLoading(false);
            }
        };

        fetchConfig();
    }, []);

    return (
        <ConfigContext.Provider value={{ agents, crossmap, loading, error }}>
            {children}
        </ConfigContext.Provider>
    );
};

export const useConfig = () => {
    const context = useContext(ConfigContext);
    if (context === undefined) {
        throw new Error('useConfig must be used within a ConfigProvider');
    }
    return context;
};
