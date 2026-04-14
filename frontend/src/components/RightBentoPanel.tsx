
import React from 'react';
import { BENTO_METADATA } from '../constants';

interface RightBentoPanelProps {
    collapsed: boolean;
    setCollapsed: (v: boolean) => void;
}

const V03_CHANGES = [
    { label: 'Zero-Hallucination Engine', detail: 'Faithfulness validation strips ungrounded citations before they reach you.' },
    { label: 'Smarter Embeddings', detail: 'Switched to gemini-embedding-001 (768-dim) — sharper retrieval, lower L2 scores.' },
    { label: '4 Specialist Agents', detail: 'Lean routing: NIST Controls, Audit, Risk, Compliance — no bloat.' },
    { label: '140 Automated Tests', detail: 'Backend coverage >80 %, CI gates on every push.' },
    { label: 'Hardened Security', detail: 'Rate limiting, timing-safe auth, no stack traces in responses.' },
];

const RightBentoPanel: React.FC<RightBentoPanelProps> = ({ collapsed, setCollapsed }) => {
    return (
        <aside className={`${collapsed ? 'w-12 bg-transparent border-none' : 'w-[420px] bg-brand-dark/95 backdrop-blur-xl border-l border-white/10'} transition-all duration-500 flex flex-col h-full overflow-y-auto custom-scrollbar`}>
            <div className={`flex items-center ${collapsed ? 'justify-center py-4' : 'justify-between px-5 py-4'}`}>
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="p-2 hover:bg-white/10 rounded-full text-brand-cyan transition-colors bg-brand-dark/50 border border-white/5 shadow-lg"
                    title={collapsed ? "Expand Insights" : "Collapse"}
                >
                    {collapsed ? '→' : '←'}
                </button>
                {!collapsed && <p className="text-xs font-black uppercase tracking-[0.35em] text-gray-500">Insights</p>}
            </div>

            {!collapsed && (
                <div className="px-4 space-y-3 pb-6">
                    {/* Profile Image Card */}
                    <div className="relative aspect-[4/3] rounded-xl overflow-hidden group cursor-pointer">
                        <img
                            src="/image/pic_owe2.jpg"
                            alt="Profile"
                            className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-1000"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-[#0B0C10] via-[#0B0C10]/40 to-transparent"></div>
                        <div className="absolute bottom-4 left-4">
                            <p className="text-[10px] font-black uppercase tracking-[0.3em] text-brand-cyan mb-0.5">Profile</p>
                            <h3 className="text-base font-black text-white tracking-tight leading-tight">Rudy Prasetiya</h3>
                        </div>
                    </div>

                    {/* About This Project */}
                    <div className="p-4 rounded-xl bg-white/5 border border-white/5 hover:border-brand-cyan/20 transition-all">
                        <h4 className="text-[11px] font-black uppercase tracking-[0.2em] text-brand-cyan mb-2">About This Project</h4>
                        <p className="text-[13px] text-gray-300 font-medium leading-relaxed mb-2">
                            AI-powered knowledge system for <span className="text-white font-bold">NIST SP 800-53</span> — RAG + multi-agent orchestration + FAISS vector search across 1,189 controls.
                        </p>
                        <div className="space-y-1.5">
                            <div className="flex items-start gap-2">
                                <span className="w-1.5 h-1.5 rounded-full bg-brand-purple mt-1.5 shrink-0"></span>
                                <p className="text-xs text-gray-400 leading-snug"><span className="text-white font-semibold">4 specialist agents</span> — auto-routed by intent</p>
                            </div>
                            <div className="flex items-start gap-2">
                                <span className="w-1.5 h-1.5 rounded-full bg-brand-cyan mt-1.5 shrink-0"></span>
                                <p className="text-xs text-gray-400 leading-snug"><span className="text-white font-semibold">Cross-framework</span> — FedRAMP, CMMC, ISO 27001</p>
                            </div>
                            <div className="flex items-start gap-2">
                                <span className="w-1.5 h-1.5 rounded-full bg-brand-purple mt-1.5 shrink-0"></span>
                                <p className="text-xs text-gray-400 leading-snug"><span className="text-white font-semibold">Audit-ready citations</span> — source docs + page #</p>
                            </div>
                        </div>
                    </div>

                    {/* What's New — v03 */}
                    <div className="p-4 rounded-xl border border-brand-cyan/20 bg-gradient-to-br from-brand-cyan/5 to-transparent">
                        <div className="flex items-center gap-2 mb-2.5">
                            <span className="px-2 py-0.5 text-[10px] font-black uppercase tracking-wider bg-brand-cyan/20 text-brand-cyan rounded-full">v03</span>
                            <h4 className="text-[11px] font-black uppercase tracking-[0.15em] text-brand-cyan">What Changed</h4>
                        </div>
                        <div className="space-y-2">
                            {V03_CHANGES.map((item, i) => (
                                <div key={i} className="flex items-start gap-2">
                                    <span className="text-brand-cyan text-xs mt-0.5 shrink-0">›</span>
                                    <p className="text-xs text-gray-300 leading-snug">
                                        <span className="text-white font-semibold">{item.label}</span>
                                        <span className="text-gray-500"> — </span>
                                        {item.detail}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Value Proposition */}
                    <div className="p-4 rounded-xl border border-white/5 bg-gradient-to-br from-brand-purple/10 to-brand-cyan/5 hover:border-brand-purple/20 transition-all">
                        <h4 className="text-[11px] font-black uppercase tracking-[0.2em] text-brand-purple mb-2">Why This Matters</h4>
                        <p className="text-[13px] text-gray-300 font-medium leading-relaxed mb-1.5">
                            Organizations managing <span className="text-white font-bold">federal systems or government contracts</span> must demonstrate NIST 800-53 compliance — or risk losing ATO.
                        </p>
                        <p className="text-xs text-gray-500 leading-snug">
                            Transforms internal audit into <span className="text-brand-cyan font-medium">strategic partnership</span> — bridging cybersecurity, data science, and product management.
                        </p>
                    </div>

                    {/* Strategic Pillar Card */}
                    <div className="bg-brand-purple rounded-xl p-4 text-white shadow-xl shadow-brand-purple/20 hover:scale-[1.01] transition-transform">
                        <p className="text-[10px] font-black uppercase tracking-[0.35em] mb-1.5 opacity-70">Metric Impact</p>
                        <h3 className="text-xl font-black mb-1 tracking-tighter uppercase leading-none">Strategic Oversight.</h3>
                        <p className="text-xs font-semibold mt-1 opacity-80">Managing global compliance for enterprise public sectors.</p>
                    </div>

                    {/* Bento Boxes */}
                    {BENTO_METADATA.map(bento => (
                        <div key={bento.id} className="p-4 rounded-xl bg-white/5 border border-white/5 hover:border-white/10 transition-all group">
                            <div className="flex items-center justify-between mb-1.5">
                                <h4 className="text-[11px] font-black uppercase tracking-[0.2em]" style={{ color: bento.accent }}>{bento.title}</h4>
                                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: bento.accent }}></div>
                            </div>
                            <p className="text-[13px] text-gray-400 font-medium leading-relaxed group-hover:text-gray-200 transition-colors">
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
