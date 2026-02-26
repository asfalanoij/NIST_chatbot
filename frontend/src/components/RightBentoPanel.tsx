
import React from 'react';
import { BENTO_METADATA } from '../constants';

interface RightBentoPanelProps {
    collapsed: boolean;
    setCollapsed: (v: boolean) => void;
}

const RightBentoPanel: React.FC<RightBentoPanelProps> = ({ collapsed, setCollapsed }) => {
    return (
        <aside className={`${collapsed ? 'w-12 bg-transparent border-none' : 'w-80 bg-brand-dark/95 backdrop-blur-xl border-l border-white/10'} transition-all duration-500 flex flex-col h-full overflow-y-auto custom-scrollbar`}>
            <div className={`flex items-center ${collapsed ? 'justify-center py-4' : 'justify-between px-4 py-4'}`}>
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="p-2 hover:bg-white/10 rounded-full text-brand-cyan transition-colors bg-brand-dark/50 border border-white/5 shadow-lg"
                    title={collapsed ? "Expand Insights" : "Collapse"}
                >
                    {collapsed ? '→' : '←'}
                </button>
                {!collapsed && <p className="text-[10px] font-black uppercase tracking-[0.4em] text-gray-500">Insights</p>}
            </div>

            {!collapsed && (
                <div className="px-3 space-y-2.5 pb-4">
                    {/* Profile Image Card */}
                    <div className="relative aspect-[4/3] rounded-xl overflow-hidden group cursor-pointer">
                        <img
                            src="/image/pic_owe2.jpg"
                            alt="Profile"
                            className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-1000"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-[#0B0C10] via-[#0B0C10]/40 to-transparent"></div>
                        <div className="absolute bottom-3 left-3">
                            <p className="text-[8px] font-black uppercase tracking-[0.3em] text-brand-cyan mb-0.5">Profile</p>
                            <h3 className="text-sm font-black text-white tracking-tight leading-tight">Rudy Prasetiya</h3>
                        </div>
                    </div>

                    {/* About This Project */}
                    <div className="p-3 rounded-xl bg-white/5 border border-white/5 hover:border-brand-cyan/20 transition-all">
                        <h4 className="text-[8px] font-black uppercase tracking-[0.2em] text-brand-cyan mb-1.5">About This Project</h4>
                        <p className="text-[10px] text-gray-300 font-medium leading-[1.5] mb-1.5">
                            AI-powered knowledge system for <span className="text-white font-bold">NIST SP 800-53</span> — RAG + multi-agent orchestration + FAISS vector search across 1,189 controls.
                        </p>
                        <div className="space-y-1">
                            <div className="flex items-start gap-1.5">
                                <span className="w-1 h-1 rounded-full bg-brand-purple mt-1 shrink-0"></span>
                                <p className="text-[9px] text-gray-400 leading-snug"><span className="text-white">5 specialist agents</span> — auto-routed by intent</p>
                            </div>
                            <div className="flex items-start gap-1.5">
                                <span className="w-1 h-1 rounded-full bg-brand-cyan mt-1 shrink-0"></span>
                                <p className="text-[9px] text-gray-400 leading-snug"><span className="text-white">Cross-framework</span> — FedRAMP, CMMC, ISO 27001</p>
                            </div>
                            <div className="flex items-start gap-1.5">
                                <span className="w-1 h-1 rounded-full bg-brand-purple mt-1 shrink-0"></span>
                                <p className="text-[9px] text-gray-400 leading-snug"><span className="text-white">Audit-ready citations</span> — source docs + page #</p>
                            </div>
                        </div>
                    </div>

                    {/* Value Proposition */}
                    <div className="p-3 rounded-xl border border-white/5 bg-gradient-to-br from-brand-purple/10 to-brand-cyan/5 hover:border-brand-purple/20 transition-all">
                        <h4 className="text-[8px] font-black uppercase tracking-[0.2em] text-brand-purple mb-1.5">Why This Matters</h4>
                        <p className="text-[10px] text-gray-300 font-medium leading-[1.5] mb-1">
                            Organizations managing <span className="text-white font-bold">federal systems or government contracts</span> must demonstrate NIST 800-53 compliance — or risk losing ATO.
                        </p>
                        <p className="text-[9px] text-gray-500 leading-snug">
                            Transforms internal audit into <span className="text-brand-cyan">strategic partnership</span> — bridging cybersecurity, data science, and product management.
                        </p>
                    </div>

                    {/* Strategic Pillar Card */}
                    <div className="bg-brand-purple rounded-xl p-3.5 text-white shadow-xl shadow-brand-purple/20 hover:scale-[1.02] transition-transform">
                        <p className="text-[8px] font-black uppercase tracking-[0.4em] mb-1 opacity-70">Metric Impact</p>
                        <h3 className="text-lg font-black mb-0.5 tracking-tighter uppercase leading-none">Strategic Oversight.</h3>
                        <p className="text-[8px] font-bold mt-1 opacity-80">Managing global compliance for enterprise public sectors.</p>
                    </div>

                    {/* Bento Boxes */}
                    {BENTO_METADATA.map(bento => (
                        <div key={bento.id} className="p-3 rounded-xl bg-white/5 border border-white/5 hover:border-white/10 transition-all group">
                            <div className="flex items-center justify-between mb-1">
                                <h4 className="text-[8px] font-black uppercase tracking-[0.2em]" style={{ color: bento.accent }}>{bento.title}</h4>
                                <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: bento.accent }}></div>
                            </div>
                            <p className="text-[10px] text-gray-400 font-medium leading-relaxed group-hover:text-gray-200 transition-colors">
                                {bento.content}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </aside>
    );
};

export default RightBentoPanel;
