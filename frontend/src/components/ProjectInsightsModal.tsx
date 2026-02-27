import { useState } from 'react';
import { X, Brain, Shield, Cpu, Layers } from 'lucide-react';

interface ProjectInsightsModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function ProjectInsightsModal({ isOpen, onClose }: ProjectInsightsModalProps) {
    const [activeTab, setActiveTab] = useState<'arch' | 'ds' | 'audit'>('arch');

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="w-full max-w-4xl bg-[#0f111a] border border-white/10 rounded-2xl shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
                {/* Header */}
                <div className="p-6 border-b border-white/5 flex items-center justify-between bg-[#13141c]">
                    <h2 className="text-xl font-bold text-white flex items-center gap-3">
                        <Cpu className="w-6 h-6 text-brand-purple" />
                        Project Architecture & Insights
                    </h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
                        <X className="w-6 h-6" />
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex border-b border-white/5 bg-[#13141c]/50">
                    <button
                        onClick={() => setActiveTab('arch')}
                        className={`px-6 py-4 text-sm font-medium transition-colors border-b-2 ${activeTab === 'arch' ? 'border-brand-purple text-white' : 'border-transparent text-gray-500 hover:text-gray-300'}`}
                    >
                        Architecture
                    </button>
                    <button
                        onClick={() => setActiveTab('ds')}
                        className={`px-6 py-4 text-sm font-medium transition-colors border-b-2 ${activeTab === 'ds' ? 'border-brand-cyan text-white' : 'border-transparent text-gray-500 hover:text-gray-300'}`}
                    >
                        DS & NLP
                    </button>
                    <button
                        onClick={() => setActiveTab('audit')}
                        className={`px-6 py-4 text-sm font-medium transition-colors border-b-2 ${activeTab === 'audit' ? 'border-emerald-400 text-white' : 'border-transparent text-gray-500 hover:text-gray-300'}`}
                    >
                        Audit Readiness
                    </button>
                </div>

                {/* Content */}
                <div className="p-8 overflow-y-auto custom-scrollbar flex-1 bg-[#0b0c10]">
                    {activeTab === 'arch' && (
                        <div className="space-y-6">
                            <div className="font-mono text-xs md:text-sm text-white bg-black p-6 rounded-xl border border-white/10 overflow-auto shadow-inner h-[400px] whitespace-pre">
                                {`NIST-Chatbot
├── 🖥️ Frontend (React + Tailwind)
│   ├── 💬 Chat Interface (WebSocket/REST)
│   ├── 🤖 Specialist Agents UI
│   └── 📊 Visualization (Bento Grids)
│
├── ⚙️ Backend (Flask API)
│   ├── 🔄 Ingestion Pipeline
│   │   ├── 📄 PDF Loader (PyPDF)
│   │   └── ✂️ Recursive Chunking (2k chars)
│   │
│   ├── 🧠 RAG Engine
│   │   ├── 🔍 FAISS Vector Store
│   │   ├── 🔌 Embeddings (HuggingFace)
│   │   └── 🤖 LLM Integration (Gemini/Ollama)
│   │
│   └── 🛠️ Utilities
│       └── 🚦 Rate Limiter & Cache
│
└── 💾 Data Layer
    ├── 📚 NIST SP Documents
    └── 🗂️ Vector Indices`}
                            </div>
                            <p className="text-sm text-gray-400 italic text-center">
                                High-Level System Architecture utilizing a modern RAG stack.
                            </p>
                        </div>
                    )}

                    {activeTab === 'ds' && (
                        <div className="grid md:grid-cols-2 gap-8">
                            <div className="space-y-4">
                                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                                    <Brain className="w-5 h-5 text-brand-cyan" />
                                    Strengths & Best Practices
                                </h3>
                                <ul className="space-y-3">
                                    <li className="bg-white/5 p-4 rounded-xl border border-white/5">
                                        <span className="text-brand-cyan font-bold block mb-1">Context-Aware Chunking</span>
                                        <p className="text-xs text-gray-400">Implemented 2000-character chunks with 300-char overlap to ensure complete NIST Control Families are captured together, avoiding context fragmentation.</p>
                                    </li>
                                    <li className="bg-white/5 p-4 rounded-xl border border-white/5">
                                        <span className="text-brand-cyan font-bold block mb-1">Hybrid Retrieval</span>
                                        <p className="text-xs text-gray-400">Combines dense vector similarity (FAISS) with keyword matching to handle specific regulatory codes (e.g., "AC-2(1)") effectively.</p>
                                    </li>
                                </ul>
                            </div>
                            <div className="space-y-4">
                                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                                    <Layers className="w-5 h-5 text-red-400" />
                                    Challenges Overcome
                                </h3>
                                <ul className="space-y-3">
                                    <li className="bg-white/5 p-4 rounded-xl border border-white/5">
                                        <span className="text-red-400 font-bold block mb-1">Complex PDF Structure</span>
                                        <p className="text-xs text-gray-400">Parsing nested tables and multi-column layouts in NIST 800-53 documents required custom pre-processing logic to linearize content without losing hierarchy.</p>
                                    </li>
                                    <li className="bg-white/5 p-4 rounded-xl border border-white/5">
                                        <span className="text-red-400 font-bold block mb-1">Semantic Ambiguity</span>
                                        <p className="text-xs text-gray-400">Distinguishing between "Organization-defined parameters" and actual requirements necessitated fine-tuned prompt engineering.</p>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    )}

                    {activeTab === 'audit' && (
                        <div className="space-y-6">
                            <div className="bg-emerald-500/10 border border-emerald-500/20 p-6 rounded-xl">
                                <h3 className="text-lg font-bold text-emerald-400 mb-4 flex items-center gap-2">
                                    <Shield className="w-5 h-5" />
                                    Audit Readiness Strategy
                                </h3>
                                <div className="grid md:grid-cols-3 gap-6">
                                    <div>
                                        <h4 className="font-bold text-white text-sm mb-2">Evidence Collection</h4>
                                        <p className="text-xs text-gray-400">Automated mapping of controls to required artifact types (configs, screenshots, policies).</p>
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white text-sm mb-2">53A Test Procedures</h4>
                                        <p className="text-xs text-gray-400">Integration with NIST 800-53A assessment cases to generate pre-filled test plans.</p>
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white text-sm mb-2">Gap Analysis</h4>
                                        <p className="text-xs text-gray-400">Real-time identification of missing implementations based on current system state inputs.</p>
                                    </div>
                                </div>
                            </div>

                            <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                                <h4 className="text-sm font-bold text-white mb-2">Just my two cents</h4>
                                <p className="text-xs text-gray-400 italic">"The biggest bottleneck in ATOs is the disconnect between technical data and compliance language. This tool bridges that gap by treating compliance as a code-first problem." - Rudy Prasetiya</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
