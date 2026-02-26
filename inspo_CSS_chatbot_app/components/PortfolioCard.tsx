
import React from 'react';
import type { PortfolioItem } from '../types';

interface PortfolioCardProps {
  item: PortfolioItem;
}

const PortfolioCard: React.FC<PortfolioCardProps> = ({ item }) => {
  const isSpecialDarkCard = item.isDark;

  const standardClasses = "bg-white dark:bg-[#1E202B] text-gray-900 dark:text-white border border-gray-200 dark:border-white/5 hover:border-gray-400 dark:hover:border-white/20 hover:bg-gray-50 dark:hover:bg-[#252836]";
  const specialClasses = "bg-[#5D5CDE] text-white shadow-2xl shadow-indigo-900/40 border border-transparent hover:scale-[1.02]";

  const cardClasses = isSpecialDarkCard ? specialClasses : standardClasses;
  const descriptionColor = isSpecialDarkCard ? 'text-indigo-100' : 'text-gray-500 dark:text-gray-400';
  const iconBg = isSpecialDarkCard ? 'bg-white/20' : 'bg-gray-100 dark:bg-[#13141C]';

  return (
    <div className={`rounded-3xl p-8 flex flex-col justify-between h-full min-h-[250px] transition-all duration-500 transform ${cardClasses}`}>
      
      <div className="flex justify-between items-start mb-6">
        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center text-xs font-black transition-all duration-500 ${iconBg} shadow-inner`}>
           {item.id < 10 ? `0${item.id}` : item.id}
        </div>
        
        {isSpecialDarkCard && (
            <span className="bg-white/90 backdrop-blur-sm text-[#5D5CDE] text-[9px] font-black px-3 py-1 rounded-full shadow-sm tracking-[0.2em]">DIRECTOR'S BRIEF</span>
        )}
      </div>

      <div>
        <h3 className="font-black text-xl leading-tight mb-3 tracking-tighter uppercase">{item.title}</h3>
        <p className={`text-xs font-medium leading-relaxed ${descriptionColor}`}>{item.description}</p>
      </div>

      <div className={`mt-8 pt-6 border-t flex justify-between items-center ${isSpecialDarkCard ? 'border-white/10' : 'border-gray-100 dark:border-white/5'}`}>
         <span className={`text-[10px] font-black uppercase tracking-[0.3em] ${isSpecialDarkCard ? 'text-white/80' : 'text-gray-400 dark:text-gray-500'}`}>
             {item.buttonText}
         </span>
         <a 
           href={item.buttonLink} 
           className={`w-10 h-10 rounded-full flex items-center justify-center transition-all duration-500 hover:scale-110 shadow-lg ${isSpecialDarkCard ? 'bg-white text-[#5D5CDE]' : 'bg-gray-900 dark:bg-white text-white dark:text-gray-900'}`}
         >
            <svg className="w-4 h-4 transform group-hover:-translate-y-1 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
         </a>
      </div>
    </div>
  );
};

export default PortfolioCard;
