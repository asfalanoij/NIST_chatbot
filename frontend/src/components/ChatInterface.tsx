
import React, { useState, useRef, useEffect } from 'react';
import { Sparkles, Send, Shield, BookOpen, AlertTriangle, ClipboardCheck, GitBranch } from 'lucide-react';
import MessageBubble from './MessageBubble';

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
    { icon: GitBranch, label: "FedRAMP Mapping", prompt: "How do NIST 800-53 controls map to FedRAMP requirements?" }
];

const ChatInterface = (): React.ReactNode => {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [llmBackend, setLlmBackend] = useState<string>('...')
    const endRef = useRef<HTMLDivElement>(null)

    const apiKey = import.meta.env.VITE_API_KEY || ''

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    useEffect(() => {
        fetch('http://localhost:5051/api/health')
            .then(res => res.json())
            .then(data => setLlmBackend(data.llm_backend === 'gemini' ? 'Gemini' : 'Ollama'))
            .catch(() => setLlmBackend('Offline'))
    }, [])

    const sendMessage = async (text: string) => {
        if (!text.trim()) return

        const userMsg: Message = { role: 'user', content: text }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setLoading(true)

        try {
            const headers: Record<string, string> = { 'Content-Type': 'application/json' }
            if (apiKey) headers['X-API-Key'] = apiKey

            const response = await fetch('http://localhost:5051/api/chat', {
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
                content: `Connection error. Make sure the backend is running on port 5051.\n\n\`${error instanceof Error ? error.message : 'Network error'}\``,
            }])
        } finally {
            setLoading(false)
        }
    }

    const isEmpty = messages.length === 0;

    return (
        <div className="flex flex-col h-full relative">
            {/* Top Header Bar */}
            <div className="h-16 border-b border-white/5 px-8 flex items-center justify-between bg-brand-dark/20 backdrop-blur-md sticky top-0 z-40">
                <div className="flex items-center gap-4">
                    <div className="text-[10px] font-black uppercase tracking-[0.4em] text-gray-500">System Ready</div>
                    <div className="h-4 w-px bg-white/10"></div>
                    <div className="text-[10px] font-black uppercase tracking-[0.4em] text-brand-cyan flex items-center gap-2">
                        <Sparkles className="w-3 h-3" />
                        RAG + {llmBackend}
                    </div>
                </div>
                <div className="flex gap-4">
                    <button onClick={() => setMessages([])} className="text-[10px] font-black uppercase tracking-widest text-gray-500 hover:text-white transition-colors">Clear</button>
                    {/* <button className="text-[10px] font-black uppercase tracking-widest text-gray-500 hover:text-white transition-colors">Settings</button> */}
                </div>
            </div>

            {/* Chat Area */}
            <div className={`flex-grow overflow-y-auto custom-scrollbar p-6 md:p-12 flex flex-col ${isEmpty ? 'items-center justify-center' : ''}`}>

                {isEmpty ? (
                    <>
                        <div className="max-w-2xl w-full text-center mb-12">
                            <div className="w-16 h-16 bg-brand-purple rounded-2xl mx-auto mb-6 flex items-center justify-center shadow-2xl shadow-brand-purple/20 rotate-12">
                                <Shield className="w-8 h-8 text-white" />
                            </div>
                            <h2 className="text-4xl font-black tracking-tighter text-white mb-4">NIST 800-53 Assistant</h2>
                            <p className="text-gray-500 text-sm font-medium tracking-wide">Ask about security controls, RMF steps, audit preparation, or compliance mapping. The right specialist agent is selected automatically.</p>
                        </div>

                        {/* Suggestion Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-[1080px]">
                            {QUICK_PROMPTS.map((item, i) => (
                                <button
                                    key={i}
                                    onClick={() => sendMessage(item.prompt)}
                                    className="group p-6 rounded-[1.5rem] bg-white/5 border border-white/5 hover:border-brand-cyan/30 hover:bg-white/[0.08] transition-all text-left"
                                >
                                    <span className="text-gray-500 mb-4 block group-hover:text-brand-cyan transition-colors">
                                        <item.icon className="w-6 h-6" />
                                    </span>
                                    <h4 className="text-sm font-bold text-white mb-1 group-hover:text-brand-cyan transition-colors">{item.label}</h4>
                                    <p className="text-[10px] text-gray-500 leading-tight">{item.prompt}</p>
                                </button>
                            ))}
                        </div>
                    </>
                ) : (
                    <div className="w-full max-w-[1080px] mx-auto space-y-6 pb-24">
                        {messages.map((msg, idx) => (
                            <MessageBubble
                                key={idx}
                                message={msg}
                                relatedQuestion={msg.role === 'assistant' && idx > 0 ? messages[idx - 1].content : undefined}
                            />
                        ))}

                        {loading && (
                            <div className="flex justify-start gap-4 animate-pulse">
                                <div className="w-8 h-8 rounded-full bg-brand-purple flex items-center justify-center">
                                    <Sparkles className="w-4 h-4 text-white animate-spin" />
                                </div>
                                <div className="text-sm text-gray-400 font-medium self-center">Thinking...</div>
                            </div>
                        )}
                        <div ref={endRef} />
                    </div>
                )}
            </div>

            {/* Input Section */}
            <div className="p-8 pb-12 bg-gradient-to-t from-brand-dark/80 to-transparent absolute bottom-0 w-full z-30">
                <div className="max-w-[1080px] mx-auto relative group">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage(input)}
                        placeholder="Ask about NIST controls, risk assessment, audit prep..."
                        className="w-full bg-brand-input border border-white/5 rounded-2xl py-6 px-8 pr-16 text-white text-sm focus:outline-none focus:border-brand-cyan/50 transition-all placeholder-gray-600 shadow-2xl group-hover:bg-[#232530]"
                    />
                    <button
                        onClick={() => sendMessage(input)}
                        disabled={loading || !input.trim()}
                        className="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-xl bg-brand-purple text-white flex items-center justify-center hover:scale-110 active:scale-95 transition-all disabled:opacity-50 disabled:grayscale disabled:hover:scale-100"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatInterface;
