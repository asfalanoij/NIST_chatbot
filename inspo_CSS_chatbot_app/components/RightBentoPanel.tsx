
import React from 'react';
import { BENTO_METADATA } from '../constants';

interface RightBentoPanelProps {
  collapsed: boolean;
  setCollapsed: (v: boolean) => void;
}

const RightBentoPanel: React.FC<RightBentoPanelProps> = ({ collapsed, setCollapsed }) => {
  return (
    <aside className={`${collapsed ? 'w-20' : 'w-80'} transition-all duration-500 bg-[#0B0C10] border-l border-white/5 flex flex-col h-screen overflow-y-auto custom-scrollbar`}>
      <div className="p-6 flex items-center justify-between">
        <button 
          onClick={() => setCollapsed(!collapsed)}
          className="p-2 hover:bg-white/5 rounded-lg text-gray-500 transition-colors"
        >
          {collapsed ? '←' : '→'}
        </button>
        {!collapsed && <p className="text-[10px] font-black uppercase tracking-[0.4em] text-gray-500">Framework Insights</p>}
      </div>

      {!collapsed && (
        <div className="px-6 space-y-6 pb-12">
          {/* Main Visual Profile Refined */}
          <div className="aspect-[4/5] rounded-[2rem] overflow-hidden border border-white/5 group relative">
             <img 
               src="./image/pic_owe2.jpg" 
               className="w-full h-full object-cover grayscale transition-all duration-700 group-hover:grayscale-0" 
               alt="Rudy" 
             />
             <div className="absolute inset-0 bg-gradient-to-t from-[#0B0C10] via-transparent to-transparent opacity-80"></div>
             <div className="absolute bottom-6 left-6">
                <p className="text-[10px] font-black text-[#4AB7C3] uppercase tracking-widest mb-1">Architect</p>
                <p className="text-sm font-black text-white uppercase tracking-tighter">Rudy Prasetiya</p>
             </div>
          </div>

          {/* Bento Boxes based on Design Thinking */}
          {BENTO_METADATA.map(bento => (
            <div key={bento.id} className="p-6 rounded-[2rem] bg-white/5 border border-white/5 hover:border-white/10 transition-all group">
              <div className="flex items-center justify-between mb-4">
                 <h4 className="text-[10px] font-black uppercase tracking-[0.2em]" style={{ color: bento.accent }}>{bento.title}</h4>
                 <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: bento.accent }}></div>
              </div>
              <p className="text-xs text-gray-400 font-medium leading-relaxed group-hover:text-gray-200 transition-colors">
                {bento.content}
              </p>
            </div>
          ))}

          {/* Strategic Pillar Card (Legacy UI feel) */}
          <div className="bg-[#5D5CDE] rounded-[2.5rem] p-8 text-white shadow-2xl shadow-[#5D5CDE]/20 transform hover:scale-[1.02] transition-transform">
             <p className="text-[10px] font-black uppercase tracking-[0.4em] mb-4 opacity-70">Metric Impact</p>
             <h3 className="text-4xl font-black mb-1 tracking-tighter uppercase leading-none">Strategic Oversight.</h3>
             <p className="text-[10px] font-bold mt-4 opacity-80">Managing global compliance for enterprise public sectors.</p>
          </div>
        </div>
      )}
    </aside>
  );
};

export default RightBentoPanel;
