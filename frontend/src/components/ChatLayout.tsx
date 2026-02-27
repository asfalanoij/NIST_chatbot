import { useState, useRef, useEffect } from 'react'
import { Send, Shield, Menu, Sparkles, BookOpen, AlertTriangle, ClipboardCheck, GitBranch, Target, Users } from 'lucide-react'
import MessageBubble from './MessageBubble'
import { API_BASE } from '../config'

interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: any[];
    agent_name?: string;
    agent_id?: string;
}

const QUICK_PROMPTS = [
    { icon: BookOpen, label: "Explain AC-2", prompt: "Explain the AC-2 Account Management control and its key enhancements." },
    { icon: AlertTriangle, label: "Risk Assessment", prompt: "How do I perform a FIPS 199 security categorization for a moderate-impact system?" },
    { icon: ClipboardCheck, label: "Audit Prep", prompt: "What evidence artifacts do I need for an 800-53 assessment of access controls?" },
    { icon: GitBranch, label: "FedRAMP Mapping", prompt: "How do NIST 800-53 controls map to FedRAMP requirements?" },
    { icon: Target, label: "Compliance Roadmap", prompt: "Create a phased compliance roadmap for a moderate-impact system. Prioritize quick wins first." },
]

export default function ChatLayout() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [sidebarOpen, setSidebarOpen] = useState(true)
    const [visitorCount, setVisitorCount] = useState<number | null>(null)
    const [llmBackend, setLlmBackend] = useState<string>('...')
    const endRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    useEffect(() => {
        fetch(`${API_BASE}/api/visitors/count`)
            .then(res => res.json())
            .then(data => setVisitorCount(data.unique_visitors))
            .catch(() => { })
    }, [messages.length])

    useEffect(() => {
        fetch(`${API_BASE}/api/health`)
            .then(res => res.json())
            .then(data => setLlmBackend(data.llm_backend === 'gemini' ? 'Gemini' : 'Ollama (Local)'))
            .catch(() => setLlmBackend('Offline'))
    }, [])

    const apiKey = import.meta.env.VITE_API_KEY || ''

    const sendMessage = async (text: string) => {
        if (!text.trim()) return

        const userMsg: Message = { role: 'user', content: text }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setLoading(true)

        try {
            const headers: Record<string, string> = { 'Content-Type': 'application/json' }
            if (apiKey) headers['X-API-Key'] = apiKey

            const response = await fetch(`${API_BASE}/api/chat`, {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    message: text,
                    history: messages.map(m => ({ role: m.role, content: m.content })),
                }),
            })

            const data = await response.json()
            if (data.error) throw new Error(data.error)

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.answer,
                sources: data.sources,
                agent_name: data.agent_name,
                agent_id: data.agent_id,
            }])
        } catch (error) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: `Connection error. Make sure the backend is running on port 5050 and Ollama is active.\n\n\`${error instanceof Error ? error.message : 'Network error'}\``,
            }])
        } finally {
            setLoading(false)
        }
    }

    const isEmpty = messages.length === 0

    return (
        <div className="flex h-full overflow-hidden">
            {/* Sidebar */}
            <div className={`${sidebarOpen ? 'w-72' : 'w-0'} bg-slate-900 border-r border-slate-700/50 transition-all duration-300 flex flex-col overflow-hidden`}>
                <div className="p-4 border-b border-slate-700/50 flex items-center gap-2.5">
                    <Shield className="w-5 h-5 text-blue-400 flex-shrink-0" />
                    <h1 className="font-bold text-sm whitespace-nowrap tracking-tight">NIST 800-53 Chatbot</h1>
                </div>

                <div className="flex-1 p-4 overflow-y-auto">
                    <h3 className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-3">Specialist Agents</h3>
                    <div className="space-y-1.5">
                        {[
                            { color: "text-blue-400", bg: "bg-blue-500/10", name: "NIST Controls", desc: "800-53 Rev.5 & RMF" },
                            { color: "text-emerald-400", bg: "bg-emerald-500/10", name: "Audit & Assessment", desc: "Evidence & test procedures" },
                            { color: "text-amber-400", bg: "bg-amber-500/10", name: "Risk & Impact", desc: "FIPS 199 & CIA analysis" },
                            { color: "text-purple-400", bg: "bg-purple-500/10", name: "Compliance Mapping", desc: "FedRAMP, CMMC, ISO" },
                            { color: "text-rose-400", bg: "bg-rose-500/10", name: "Product Manager", desc: "Roadmaps & prioritization" },
                            { color: "text-cyan-400", bg: "bg-cyan-500/10", name: "QA & Test Strategy", desc: "Test cases & validation" },
                            { color: "text-teal-400", bg: "bg-teal-500/10", name: "DevSecOps", desc: "CI/CD & pipeline security" },
                        ].map((agent) => (
                            <div key={agent.name} className={`p-2.5 rounded-lg ${agent.bg} border border-slate-700/30`}>
                                <div className={`text-xs font-medium ${agent.color}`}>{agent.name}</div>
                                <div className="text-[10px] text-slate-500 mt-0.5">{agent.desc}</div>
                            </div>
                        ))}
                    </div>

                    <h3 className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mt-6 mb-3">Knowledge Base</h3>
                    <div className="text-xs text-slate-400 space-y-1">
                        <div className="flex items-center gap-1.5"><BookOpen className="w-3 h-3" /> NIST SP 800-53 Rev.5</div>
                        <div className="flex items-center gap-1.5"><BookOpen className="w-3 h-3" /> NIST SP 1362</div>
                        <div className="flex items-center gap-1.5"><BookOpen className="w-3 h-3" /> FedRAMP Guidelines</div>
                    </div>
                </div>

                <div className="p-3 border-t border-slate-700/50 text-center">
                    {visitorCount !== null && (
                        <div className="flex items-center justify-center gap-1 mb-1.5">
                            <Users className="w-3 h-3 text-slate-500" />
                            <span className="text-[10px] text-slate-500">{visitorCount} visitors</span>
                        </div>
                    )}
                    <div className="text-[10px] text-slate-600">Built by</div>
                    <div className="text-xs text-slate-400 font-medium">RudyPrasetiya.com</div>
                </div>
            </div>

            {/* Main Chat */}
            <div className="flex-1 flex flex-col bg-slate-800">
                <header className="h-14 border-b border-slate-700/50 flex items-center px-4 justify-between">
                    <button
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                        className="p-2 hover:bg-slate-700 rounded-lg text-slate-400 transition-colors"
                    >
                        <Menu className="w-4 h-4" />
                    </button>
                    <div className="text-xs text-slate-500 flex items-center gap-1.5">
                        <Sparkles className="w-3 h-3" />
                        RAG + {llmBackend}
                    </div>
                    <div className="w-8" />
                </header>

                <div className="flex-1 overflow-y-auto p-4 md:p-6">
                    {isEmpty ? (
                        <div className="h-full flex flex-col items-center justify-center max-w-lg mx-auto">
                            <Shield className="w-12 h-12 text-blue-500/30 mb-4" />
                            <h2 className="text-xl font-bold text-slate-200 mb-1">NIST 800-53 Assistant</h2>
                            <p className="text-sm text-slate-500 text-center mb-8">
                                Ask about security controls, RMF steps, audit preparation, or compliance mapping.
                                The right specialist agent is selected automatically.
                            </p>
                            <div className="grid grid-cols-2 gap-2 w-full">
                                {QUICK_PROMPTS.map((qp) => (
                                    <button
                                        key={qp.label}
                                        onClick={() => sendMessage(qp.prompt)}
                                        className="text-left p-3 rounded-xl bg-slate-700/50 hover:bg-slate-700 border border-slate-600/30 transition-colors group"
                                    >
                                        <qp.icon className="w-4 h-4 text-blue-400 mb-1.5 group-hover:text-blue-300" />
                                        <div className="text-xs font-medium text-slate-300">{qp.label}</div>
                                        <div className="text-[10px] text-slate-500 mt-0.5 line-clamp-2">{qp.prompt}</div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-5 max-w-4xl mx-auto">
                            {messages.map((msg, idx) => (
                                <MessageBubble key={idx} message={msg} />
                            ))}
                            {loading && (
                                <div className="flex justify-start gap-3">
                                    <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
                                        <Sparkles className="w-4 h-4 text-white animate-spin" />
                                    </div>
                                    <div className="bg-slate-700 rounded-2xl rounded-bl-sm px-4 py-3 shadow-lg">
                                        <div className="flex items-center gap-1.5">
                                            <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                                            <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                                            <div className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={endRef} />
                        </div>
                    )}
                </div>

                <div className="p-3 border-t border-slate-700/50 bg-slate-800/80">
                    <div className="max-w-4xl mx-auto flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage(input)}
                            placeholder="Ask about NIST controls, risk assessment, audit prep..."
                            disabled={loading}
                            className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 placeholder-slate-500 transition-all"
                        />
                        <button
                            onClick={() => sendMessage(input)}
                            disabled={loading || !input.trim()}
                            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-30 disabled:cursor-not-allowed text-white px-3.5 rounded-xl transition-colors flex items-center justify-center"
                        >
                            <Send className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
