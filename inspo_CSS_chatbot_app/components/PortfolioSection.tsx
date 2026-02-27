
import React from 'react';
import { PORTFOLIO_ITEMS } from '../constants';
import PortfolioCard from './PortfolioCard';

const PortfolioSection = (): React.ReactNode => {
  return (
    <section className="mt-32">
      <div className="mb-16 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
         <h2 className="text-2xl md:text-3xl font-black text-gray-900 dark:text-white uppercase tracking-tighter">
            Thought <span className="text-[#4AB7C3]">&</span> Leadership.
         </h2>
         <div className="flex-grow hidden md:block h-px bg-gradient-to-r from-gray-800 to-transparent mx-10"></div>
         <p className="text-xs font-bold text-gray-500 uppercase tracking-[0.3em]">Advocating for digital resilience</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8">
        {/* Leadership Stat Block */}
        <div className="bg-[#4AB7C3] rounded-3xl p-8 flex flex-col justify-between text-gray-900 col-span-1 min-h-[250px] shadow-xl transform hover:scale-[1.02] transition-transform duration-500">
           <div>
              <p className="text-[10px] font-black uppercase tracking-[0.4em] mb-4 opacity-70">Impact Metrics</p>
              <span className="text-5xl font-black mb-1 block tracking-tighter">8.2k+</span>
              <span className="text-xs font-bold uppercase tracking-widest">Audit Nodes Verified</span>
           </div>
           
           <div className="mt-8 flex items-center justify-between">
              <div className="w-12 h-12 bg-white/30 rounded-full flex items-center justify-center backdrop-blur-md">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.84 9.49.5.09.68-.21.68-.47 0-.23-.01-.86-.01-1.68-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02a9.58 9.58 0 012.5-.34c.85.01 1.7.11 2.5.34 1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85 0 1.34-.01 2.42-.01 2.75 0 .27.18.57.69.47C21.14 20.17 24 16.42 24 12c0-5.523-4.477-10-10-10z"/></svg>
              </div>
              <span className="text-[10px] font-black uppercase tracking-widest">Active Governance</span>
           </div>
        </div>

        {PORTFOLIO_ITEMS.map(item => (
          <PortfolioCard key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
};

export default PortfolioSection;
