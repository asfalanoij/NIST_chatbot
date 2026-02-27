import { User, Bot, FileText, Copy, Printer, Check } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { useState, useRef } from 'react'

interface MessageBubbleProps {
    message: {
        role: 'user' | 'assistant';
        content: string;
        sources?: Array<{
            source: string;
            page: number | string;
            content_snippet: string;
        }>;
        agent_name?: string;
    };
    relatedQuestion?: string;
}

export default function MessageBubble({ message, relatedQuestion }: MessageBubbleProps) {
    const isUser = message.role === 'user'
    const [copied, setCopied] = useState(false)

    const handleCopy = () => {
        navigator.clipboard.writeText(message.content)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    const contentRef = useRef<HTMLDivElement>(null)

    const handlePrint = () => {
        const printWindow = window.open('', '_blank')
        if (printWindow) {
            // Write the HTML structure (Safe from backticks in content)
            printWindow.document.write(`
                <html>
                    <head>
                        <title>NIST Chatbot - Q&A Export</title>
                        <style>
                            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400&display=swap');
                            body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; color: #333; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                            
                            .container { display: flex; min-height: 100vh; }
                            
                            /* Left Sidebar styling (2cm ~ 75px) */
                            .sidebar { 
                                width: 75px; 
                                background-image: url('/image/sea_bg03.jpg');
                                background-size: cover;
                                background-position: center;
                                color: #0f172a; 
                                padding: 20px 5px; 
                                box-sizing: border-box;
                                display: flex; 
                                flex-direction: column;
                                align-items: center;
                                border-right: 1px solid #cbd5e1;
                                text-align: center;
                            }
                            
                            .rp-logo { 
                                width: 40px; height: 40px; 
                                background: linear-gradient(135deg, #06b6d4, #8b5cf6); 
                                border-radius: 50%; 
                                display: flex; align-items: center; justify-content: center; 
                                font-weight: 800; font-size: 14px; color: white; 
                                margin-bottom: 30px;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                            }
                            
                            .sidebar-text-vertical {
                                writing-mode: vertical-rl;
                                text-orientation: mixed;
                                transform: rotate(180deg);
                                font-size: 10px;
                                font-weight: 800;
                                letter-spacing: 2px;
                                text-transform: uppercase;
                                color: #1e293b;
                                margin: 20px 0;
                                flex-grow: 1;
                                text-shadow: 0 1px 2px rgba(255,255,255,0.5);
                            }

                            .contact-icon { font-size: 16px; margin-bottom: 5px; color: #0e7490; }
                            .contact-group { margin-top: auto; display: flex; flex-direction: column; gap: 15px; margin-bottom: 20px; }
                            
                            /* Main Content styling */
                            .main { flex: 1; padding: 40px 50px; background: white; display: flex; flex-direction: column; }
                            
                            .header { border-bottom: 2px solid #0f111a; padding-bottom: 15px; margin-bottom: 30px; }
                            .doc-title { font-size: 16px; font-weight: 800; color: #0f111a; text-transform: uppercase; letter-spacing: 0.5px; }
                            
                            .qa-section { flex-grow: 1; }
                            
                            .question-box {
                                background: #f1f5f9;
                                border-left: 4px solid #64748b;
                                padding: 15px 20px;
                                margin-bottom: 25px;
                                border-radius: 0 8px 8px 0;
                            }
                            .q-label { font-size: 9px; uppercase; font-weight: 800; color: #64748b; margin-bottom: 5px; tracking-widest; letter-spacing: 1px; }
                            .q-text { font-size: 12px; font-weight: 600; color: #0f111a; }
                            
                            .answer-box { margin-bottom: 30px; }
                            .a-label { font-size: 9px; uppercase; font-weight: 800; color: #06b6d4; margin-bottom: 10px; tracking-widest; letter-spacing: 1px; }
                            .a-text { font-size: 11px; line-height: 1.6; color: #334155; }
                            .a-text p { margin-bottom: 10px; }
                            .a-text ul { padding-left: 20px; margin-bottom: 10px; }
                            .a-text li { margin-bottom: 4px; }

                            .technical-footer {
                                margin-top: 40px;
                                padding-top: 20px;
                                border-top: 1px dotted #cbd5e1;
                            }
                            .footer-title { font-size: 8px; font-weight: 800; text-transform: uppercase; color: #94a3b8; margin-bottom: 10px; }
                            .ascii-tree {
                                font-family: 'JetBrains Mono', monospace;
                                font-size: 6pt;
                                line-height: 1.2;
                                white-space: pre;
                                color: #475569;
                                background: #f8fafc;
                                padding: 10px;
                                border-radius: 4px;
                                border: 1px solid #e2e8f0;
                            }
                            
                            .contact-stripe {
                                font-size: 8px;
                                color: #64748b;
                                margin-top: 20px;
                                text-align: right;
                                font-family: 'JetBrains Mono', monospace;
                            }

                            /* Hide URL/Page info in print if browser settings allow */
                            @page { margin: 0; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <!-- Sidebar -->
                            <div class="sidebar">
                                <div class="rp-logo">RP</div>
                                <div class="sidebar-text-vertical">Project Oversight • Audit • GRC</div>
                                <div class="contact-group">
                                    <div style="font-size: 8px; color: #334155; writing-mode: vertical-rl; transform: rotate(180deg); font-weight: 600;">rudyhendra@iuj.ac.jp</div>
                                    <div style="font-size: 8px; color: #334155; writing-mode: vertical-rl; transform: rotate(180deg); font-weight: 600;">linkedin.com/in/rudyprasetiya</div>
                                    <div style="font-size: 8px; color: #334155; writing-mode: vertical-rl; transform: rotate(180deg); font-weight: 600;">rudyprasetiya.com</div>
                                </div>
                            </div>
                            
                            <!-- Main Content -->
                            <div class="main">
                                <div class="header">
                                    <div class="doc-title">NIST 800-53 Chatbot | rudyprasetiya.com</div>
                                </div>
                                
                                <div class="qa-section">
                                    <div id="print-question-container"></div>
                                    
                                    <div class="answer-box">
                                        <div class="a-label">RESPONSE ${message.agent_name ? `• ${message.agent_name}` : ''}</div>
                                        <div class="a-text" id="print-answer-content"></div>
                                    </div>
                                </div>

                                <div class="technical-footer">
                                    <div class="footer-title">System Architecture</div>
                                    <div class="ascii-tree">NIST-Chatbot
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
└── 💾 Data Layer</div>
                                    <div class="contact-stripe">
                                        rudyhendra@iuj.ac.jp • rudyprasetiya.com • linkedin.com/in/rudyprasetiya
                                    </div>
                                </div>
                            </div>
                        </div>
                    </body>
                </html>
            `)

            // Inject content safely
            if (relatedQuestion) {
                const questionContainer = printWindow.document.getElementById('print-question-container');
                if (questionContainer) {
                    questionContainer.innerHTML = `
                        <div class="question-box">
                            <div class="q-label">QUESTION</div>
                            <div class="q-text">${relatedQuestion.replace(/`/g, '&#96;')}</div> 
                        </div>
                    `;
                }
            }

            const answerContainer = printWindow.document.getElementById('print-answer-content');
            if (answerContainer && contentRef.current) {
                answerContainer.innerHTML = contentRef.current.innerHTML;
            }

            printWindow.document.close()
            printWindow.focus()
            // Slight delay to ensure content renders
            setTimeout(() => {
                printWindow.print()
            }, 250)
        }
    }

    return (
        <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'} group`}>
            {!isUser && (
                <div className="flex flex-col items-center gap-1 flex-shrink-0">
                    <div className="w-8 h-8 rounded-full bg-brand-cyan/20 flex items-center justify-center border border-brand-cyan/50">
                        <Bot className="w-4 h-4 text-brand-cyan" />
                    </div>
                </div>
            )}

            <div className="max-w-[85%] flex flex-col">
                {!isUser && message.agent_name && (
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-brand-cyan mb-1 ml-1">
                        {message.agent_name}
                    </span>
                )}
                <div className={`rounded-2xl px-4 py-3 relative ${isUser
                    ? 'bg-brand-purple text-white rounded-br-sm shadow-xl shadow-brand-purple/10 text-[13px]'
                    : 'bg-white/5 border border-white/5 text-gray-300 rounded-bl-sm shadow-lg backdrop-blur-sm text-[12px]'
                    }`}>
                    <div
                        id={`msg-content-${message.content.substring(0, 10)}`}
                        ref={contentRef}
                        className="text-gray-300 max-w-none
                        [&_p]:text-[12px] [&_p]:leading-[1.6] [&_p]:mb-4
                        [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:mb-4
                        [&_ol]:list-decimal [&_ol]:pl-5 [&_ol]:mb-4
                        [&_li]:text-[12px] [&_li]:leading-[1.6] [&_li]:mb-3
                        [&_li_>_ul]:mt-2 [&_li_>_ul]:mb-0
                        [&_li_>_ol]:mt-2 [&_li_>_ol]:mb-0
                        [&_h1]:text-white [&_h1]:text-[13px] [&_h1]:font-bold [&_h1]:mt-4 [&_h1]:mb-2
                        [&_h2]:text-white [&_h2]:text-[13px] [&_h2]:font-bold [&_h2]:mt-4 [&_h2]:mb-2
                        [&_h3]:text-white [&_h3]:text-[13px] [&_h3]:font-bold [&_h3]:mt-4 [&_h3]:mb-2
                        [&_strong]:text-brand-cyan [&_strong]:text-[12px]
                        [&_code]:text-brand-cyan [&_code]:text-[11px] [&_code]:bg-black/30 [&_code]:px-1 [&_code]:rounded
                        [font-family:'Inter',system-ui,sans-serif]
                    ">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>

                    {message.sources && message.sources.length > 0 && (
                        <div className="mt-4 pt-3 border-t border-white/10">
                            <h4 className="text-[10px] font-black text-gray-500 mb-2 uppercase tracking-widest flex items-center gap-1">
                                <FileText className="w-3 h-3" /> Sources
                            </h4>
                            <div className="space-y-1.5">
                                {message.sources.map((src, i) => (
                                    <div key={i} className="text-xs bg-black/20 px-3 py-2 rounded-lg border border-white/5 hover:border-brand-cyan/30 transition-colors">
                                        <span className="font-bold text-brand-cyan/80">
                                            {src.source}
                                        </span>
                                        <span className="text-gray-500 ml-1">p.{src.page}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* Actions Footer */}
                {!isUser && (
                    <div className="flex items-center gap-2 mt-2 ml-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        <button
                            onClick={handleCopy}
                            className="flex items-center gap-1.5 text-[10px] text-gray-500 hover:text-brand-cyan transition-colors bg-white/5 px-2 py-1 rounded-md border border-white/5 hover:border-brand-cyan/30"
                            title="Copy to clipboard"
                        >
                            {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
                            {copied ? 'Copied' : 'Copy'}
                        </button>
                        <button
                            onClick={handlePrint}
                            className="flex items-center gap-1.5 text-[10px] text-gray-500 hover:text-brand-purple transition-colors bg-white/5 px-2 py-1 rounded-md border border-white/5 hover:border-brand-purple/30"
                            title="Print PDF"
                        >
                            <Printer className="w-3 h-3" />
                            PDF
                        </button>
                    </div>
                )}
            </div>

            {
                isUser && (
                    <div className="w-8 h-8 rounded-full bg-brand-purple/20 flex items-center justify-center flex-shrink-0 border border-brand-purple/50">
                        <User className="w-4 h-4 text-brand-purple" />
                    </div>
                )
            }
        </div >
    )
}
