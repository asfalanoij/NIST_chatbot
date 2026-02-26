
import React from 'react';

const ChatInterface = (): React.ReactNode => {
  return (
    <div className="flex flex-col h-full relative">
      {/* Top Header Bar */}
      <div className="h-16 border-b border-white/5 px-8 flex items-center justify-between">
         <div className="flex items-center gap-4">
            <div className="text-[10px] font-black uppercase tracking-[0.4em] text-gray-500">System Ready</div>
            <div className="h-4 w-px bg-white/10"></div>
            <div className="text-[10px] font-black uppercase tracking-[0.4em] text-[#4AB7C3]">RAG + Gemini 3.0 Pro</div>
         </div>
         <div className="flex gap-4">
            <button className="text-[10px] font-black uppercase tracking-widest text-gray-500 hover:text-white transition-colors">History</button>
            <button className="text-[10px] font-black uppercase tracking-widest text-gray-500 hover:text-white transition-colors">Settings</button>
         </div>
      </div>

      {/* Chat Area */}
      <div className="flex-grow overflow-y-auto p-12 flex flex-col items-center justify-center">
        <div className="max-w-2xl w-full text-center mb-12">
           <div className="w-16 h-16 bg-[#5D5CDE] rounded-2xl mx-auto mb-6 flex items-center justify-center shadow-2xl shadow-[#5D5CDE]/20 rotate-12">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
           </div>
           <h2 className="text-4xl font-black tracking-tighter text-white mb-4">NIST 800-53 Assistant</h2>
           <p className="text-gray-500 text-sm font-medium tracking-wide">Ask about security controls, RMF steps, audit preparation, or compliance mapping. The right specialist agent is selected automatically.</p>
        </div>

        {/* Suggestion Grid */}
        <div className="grid grid-cols-2 gap-4 w-full max-w-4xl">
           {[
             { title: 'Explain AC-2', desc: 'Account Management control enhancements', icon: '[]' },
             { title: 'Risk Assessment', desc: 'How do I perform a FIPS 199 categorization?', icon: '!' },
             { title: 'Audit Prep', desc: 'Evidence artifacts for access controls', icon: 'v' },
             { title: 'FedRAMP Mapping', desc: 'NIST 800-53 to FedRAMP mapping', icon: 'y' }
           ].map((item, i) => (
             <button key={i} className="group p-6 rounded-[1.5rem] bg-white/5 border border-white/5 hover:border-[#4AB7C3]/30 hover:bg-white/[0.08] transition-all text-left">
                <span className="text-gray-500 text-lg mb-2 block">{item.icon}</span>
                <h4 className="text-sm font-bold text-white mb-1">{item.title}</h4>
                <p className="text-[10px] text-gray-500 leading-tight">{item.desc}</p>
             </button>
           ))}
        </div>
      </div>

      {/* Input Section */}
      <div className="p-8 pb-12">
        <div className="max-w-4xl mx-auto relative">
           <input 
             type="text" 
             placeholder="Ask about NIST controls, risk assessment, audit prep..." 
             className="w-full bg-[#1E202B] border border-white/5 rounded-2xl py-6 px-8 text-white focus:outline-none focus:border-[#4AB7C3] transition-colors placeholder-gray-600 shadow-2xl"
           />
           <button className="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-xl bg-[#5D5CDE] text-white flex items-center justify-center hover:scale-110 transition-transform">
             ↑
           </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
