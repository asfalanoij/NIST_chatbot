
import React from 'react';
import { SPECIALIST_AGENTS, KNOWLEDGE_BASE } from '../constants';

interface SidebarProps {
  collapsed: boolean;
  setCollapsed: (v: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed, setCollapsed }) => {
  return (
    <aside className={`${collapsed ? 'w-20' : 'w-72'} transition-all duration-500 bg-[#0B0C10] flex flex-col border-r border-white/5 h-screen relative z-50`}>
      <div className="p-6 flex items-center justify-between">
        {!collapsed && (
           <h1 className="text-xl font-black tracking-tighter text-white flex items-center gap-2">
             <span className="w-2 h-2 rounded-full bg-[#5D5CDE] animate-pulse"></span>
             NIST 800-53 Chatbot
           </h1>
        )}
        <button 
          onClick={() => setCollapsed(!collapsed)}
          className="p-2 hover:bg-white/5 rounded-lg text-gray-500 transition-colors"
        >
          {collapsed ? '→' : '←'}
        </button>
      </div>

      <div className="flex-grow overflow-y-auto overflow-x-hidden px-4 py-4 custom-scrollbar">
        <div className="mb-8">
          <p className={`text-[10px] font-black uppercase tracking-[0.3em] text-gray-600 mb-4 ${collapsed ? 'text-center' : ''}`}>
            Specialist Agents
          </p>
          <div className="space-y-2">
            {SPECIALIST_AGENTS.map(agent => (
              <button key={agent.id} className="w-full group flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-all duration-300 text-left">
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-[#4AB7C3] group-hover:bg-[#4AB7C3] group-hover:text-black transition-all">
                  ●
                </div>
                {!collapsed && (
                  <div>
                    <p className="text-xs font-bold text-white leading-none">{agent.name}</p>
                    <p className="text-[10px] text-gray-500 mt-1 truncate w-40">{agent.description}</p>
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>

        <div className="mb-8">
          <p className={`text-[10px] font-black uppercase tracking-[0.3em] text-gray-600 mb-4 ${collapsed ? 'text-center' : ''}`}>
            Knowledge Base
          </p>
          {!collapsed && KNOWLEDGE_BASE.map(item => (
            <a key={item.id} href={item.link} className="flex items-center gap-3 p-3 text-xs text-gray-400 hover:text-white transition-colors">
              <span className="opacity-40">[]</span> {item.title}
            </a>
          ))}
        </div>
      </div>

      <div className="p-6 border-t border-white/5">
        {!collapsed && (
          <div className="flex flex-col gap-2">
             <div className="flex items-center gap-2 text-[10px] font-bold text-gray-500 uppercase tracking-widest">
                <span className="text-[#4AB7C3]">1.2k</span> active sessions
             </div>
             <p className="text-[10px] text-gray-600 font-medium">Built by RudyPrasetiya.com</p>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
