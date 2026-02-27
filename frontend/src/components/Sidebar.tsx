
import React, { useState } from 'react';
import { ShieldCheck, FileText, Cloud, Info, ChevronDown, ChevronRight, BarChart3 } from 'lucide-react';
import { SPECIALIST_AGENTS, KNOWLEDGE_BASE } from '../constants';
import ProjectInsightsModal from './ProjectInsightsModal';
import CrossMapModal from './CrossMapModal';

const KB_ICONS: Record<string, { icon: React.ElementType; color: string }> = {
    kb1: { icon: ShieldCheck, color: '#5D5CDE' },
    kb2: { icon: FileText, color: '#4AB7C3' },
    kb3: { icon: Cloud, color: '#E879A0' },
};

interface SidebarProps {
    collapsed: boolean;
    setCollapsed: (v: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed, setCollapsed }) => {
    const [hoveredAgent, setHoveredAgent] = useState<{ id: string; name: string; description: string; icon: string; details: string[]; top: number } | null>(null);
    const [insightsOpen, setInsightsOpen] = useState(false);
    const [crossMapOpen, setCrossMapOpen] = useState(false);
    const [isAgentsOpen, setIsAgentsOpen] = useState(false);
    return (
        <aside className={`${collapsed ? 'w-20' : 'w-72'} transition-all duration-500 bg-[url('/image/sea_bg03.jpg')] bg-cover bg-center flex flex-col border-r border-white/20 h-screen relative z-50`}>
            <div className="p-6 flex items-center justify-between">
                {!collapsed && (
                    <h1 className="text-xl font-black tracking-tighter text-slate-900 flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-brand-purple animate-pulse"></span>
                        NIST 800-53 Chatbot
                    </h1>
                )}
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="p-2 hover:bg-white/20 rounded-lg text-slate-700 transition-colors"
                >
                    {collapsed ? '→' : '←'}
                </button>
            </div>

            <div className="flex-grow overflow-y-auto overflow-x-hidden px-4 py-4 custom-scrollbar">
                {/* Stats Bento Boxes - NOW FIRST */}
                {!collapsed && (
                    <div className="grid grid-cols-2 gap-2 mb-8">
                        <div className="p-3 rounded-xl bg-white/70 backdrop-blur-md border border-white/20 hover:border-brand-purple/50 transition-all group shadow-sm">
                            <p className="text-[9px] font-black uppercase tracking-[0.2em] text-slate-600 mb-1">Controls</p>
                            <p className="text-xl font-black text-slate-900 tracking-tight">1,189</p>
                            <p className="text-[9px] text-slate-600 mt-0.5 group-hover:text-slate-800 transition-colors">800-53 Rev.5</p>
                        </div>
                        <div className="p-3 rounded-xl bg-white/70 backdrop-blur-md border border-white/20 hover:border-brand-cyan/50 transition-all group shadow-sm">
                            <p className="text-[9px] font-black uppercase tracking-[0.2em] text-slate-600 mb-1">Compliance</p>
                            <p className="text-xl font-black text-brand-cyan tracking-tight">94%</p>
                            <p className="text-[9px] text-slate-600 mt-0.5 group-hover:text-slate-800 transition-colors">Score</p>
                        </div>
                    </div>
                )}

                {/* Knowledge Base - NOW SECOND */}
                <div className="mb-8">
                    <p className={`text-[10px] font-black uppercase tracking-[0.3em] text-slate-800 mb-4 ${collapsed ? 'text-center' : ''}`}>
                        Knowledge Base
                    </p>
                    {!collapsed && KNOWLEDGE_BASE.map(item => {
                        const kb = KB_ICONS[item.id];
                        const Icon = kb?.icon || FileText;
                        const iconColor = kb?.color || '#475569';
                        return (
                            <a
                                key={item.id}
                                href={item.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-3 p-3 text-xs text-slate-700 hover:text-slate-900 transition-colors group font-medium"
                            >
                                <Icon className="w-4 h-4 shrink-0 opacity-80 group-hover:opacity-100 transition-opacity" style={{ color: iconColor }} />
                                {item.title}
                            </a>
                        );
                    })}
                </div>

                {/* Project Insights - NOW THIRD */}
                <div className="mb-8">
                    <button
                        onClick={() => setInsightsOpen(true)}
                        className={`w-full flex items-center ${collapsed ? 'justify-center' : 'justify-between'} group`}
                    >
                        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-800 group-hover:text-brand-purple transition-colors">
                            Project Insights
                        </p>
                        {!collapsed && <Info className="w-3 h-3 text-slate-600 group-hover:text-brand-purple transition-colors" />}
                    </button>
                </div>

                {/* Cross-Mapping */}
                <div className="mb-8">
                    <button
                        onClick={() => setCrossMapOpen(true)}
                        className={`w-full flex items-center ${collapsed ? 'justify-center' : 'justify-between'} group`}
                    >
                        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-800 group-hover:text-brand-cyan transition-colors">
                            Cross-Mapping
                        </p>
                        {!collapsed && <BarChart3 className="w-3 h-3 text-slate-600 group-hover:text-brand-cyan transition-colors" />}
                    </button>
                    {!collapsed && (
                        <p className="text-[9px] text-slate-600 mt-1 font-medium">ISO 27001 &bull; CSF 2.0 &bull; ISO 27005</p>
                    )}
                </div>

                {/* Specialist Agents - NOW LAST */}
                <div className="mb-8">
                    <button
                        onClick={() => setIsAgentsOpen(!isAgentsOpen)}
                        className={`w-full flex items-center justify-between group mb-4 ${collapsed ? 'justify-center' : ''}`}
                    >
                        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-800 group-hover:text-brand-cyan transition-colors">
                            Specialist Agents
                        </p>
                        {!collapsed && (
                            <div className="text-slate-600 group-hover:text-brand-cyan transition-colors">
                                {isAgentsOpen ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                            </div>
                        )}
                    </button>

                    <div className={`space-y-2 transition-all duration-300 overflow-hidden ${isAgentsOpen ? 'max-h-[500px] opacity-100' : 'max-h-0 opacity-0'}`}>
                        {SPECIALIST_AGENTS.map(agent => (
                            <button
                                key={agent.id}
                                onMouseEnter={(e) => {
                                    const rect = e.currentTarget.getBoundingClientRect();
                                    setHoveredAgent({ ...agent, top: rect.top });
                                }}
                                onMouseLeave={() => setHoveredAgent(null)}
                                className="w-full group flex items-center gap-3 p-3 rounded-xl hover:bg-white/40 transition-all duration-300 text-left relative border border-transparent hover:border-white/20"
                            >
                                <div className="w-8 h-8 rounded-lg bg-white/40 flex items-center justify-center text-brand-cyan group-hover:bg-brand-cyan group-hover:text-black transition-all shadow-sm">
                                    ●
                                </div>
                                {!collapsed && (
                                    <div>
                                        <p className="text-xs font-bold text-slate-900 leading-none">{agent.name}</p>
                                        <p className="text-[10px] text-slate-600 mt-1 truncate w-40 font-medium">{agent.description}</p>
                                    </div>
                                )}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            <div className="p-6 border-t border-white/20 bg-white/10 backdrop-blur-sm">
                {!collapsed ? (
                    <div className="flex flex-col gap-4">
                        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-600 uppercase tracking-widest">
                            <span className="text-brand-cyan">1.2k</span> active sessions
                        </div>

                        <a
                            href="https://rudyprasetiya.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[10px] text-slate-700 font-bold hover:text-brand-cyan transition-colors"
                        >
                            Built by RudyPrasetiya.com
                        </a>

                        <a
                            href="https://www.linkedin.com/in/rudyprasetiya"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/40 transition-colors group border border-transparent hover:border-white/20"
                        >
                            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-brand-cyan to-brand-purple p-[1px] shadow-sm">
                                <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center overflow-hidden">
                                    <span className="text-[10px] font-bold text-white">RP</span>
                                </div>
                            </div>
                            <div>
                                <p className="text-xs font-bold text-slate-900 group-hover:text-brand-cyan transition-colors">Rudy Prasetiya</p>
                                <p className="text-[10px] text-slate-600 font-medium">View Profile</p>
                            </div>
                        </a>
                    </div>
                ) : (
                    <a
                        href="https://www.linkedin.com/in/rudyprasetiya"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="w-8 h-8 rounded-full bg-gradient-to-tr from-brand-cyan to-brand-purple p-[1px] block mx-auto hover:scale-110 transition-transform shadow-md"
                    >
                        <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center overflow-hidden">
                            <span className="text-[10px] font-bold text-white">RP</span>
                        </div>
                    </a>
                )}
            </div>

            {/* Floating Tooltip */}
            {hoveredAgent && (
                <div
                    className="fixed z-[100] w-64 p-4 bg-brand-panel border border-brand-cyan/20 rounded-xl shadow-2xl backdrop-blur-xl animate-in fade-in zoom-in-95 duration-200"
                    style={{
                        top: hoveredAgent.top,
                        left: collapsed ? '5.5rem' : '18.5rem'
                    }}
                >
                    <div className="absolute top-6 -left-1.5 w-3 h-3 bg-brand-panel border-l border-b border-brand-cyan/20 transform rotate-45"></div>
                    <h4 className="text-white font-bold text-sm mb-2 flex items-center gap-2 border-b border-white/10 pb-2">
                        {hoveredAgent.name}
                    </h4>
                    <p className="text-[11px] text-gray-400 font-medium mb-3 italic">
                        {hoveredAgent.description}
                    </p>
                    <ul className="space-y-1.5">
                        {hoveredAgent.details?.map((detail, idx) => (
                            <li key={idx} className="text-[10px] text-gray-300 flex items-start gap-1.5">
                                <span className="text-brand-cyan mt-0.5">›</span>
                                {detail}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Project Insights Modal */}
            <ProjectInsightsModal isOpen={insightsOpen} onClose={() => setInsightsOpen(false)} />
            <CrossMapModal isOpen={crossMapOpen} onClose={() => setCrossMapOpen(false)} />
        </aside>
    );
};

export default Sidebar;
