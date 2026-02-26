
import React from 'react';

const IntroSection = (): React.ReactNode => {
  return (
    <section className="mb-20 md:mb-40 relative pt-10">
      {/* Top Layout Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-10 items-start">
        
        {/* Left Vertical Brand Mark */}
        <div className="hidden md:flex md:col-span-1 flex-col items-center justify-start space-y-12 py-10">
          <div className="h-40 w-px bg-gradient-to-b from-transparent via-gray-700 to-transparent"></div>
          <div className="transform -rotate-90 whitespace-nowrap text-[10px] uppercase tracking-[0.4em] text-gray-600 font-bold">
            STRATEGY • GOVERNANCE • LEADERSHIP
          </div>
        </div>

        {/* Center Image Area */}
        <div className="col-span-1 md:col-span-6 relative flex justify-center md:block">
          
          {/* Strategic Bubble - Top Left */}
          <div className="absolute -top-10 -left-6 md:-left-16 z-20">
            <div className="w-28 h-28 md:w-36 md:h-36 bg-[#5D5CDE] rounded-full flex flex-col items-center justify-center text-white shadow-2xl transform -rotate-6 hover:rotate-0 transition-all duration-500 text-center border-4 border-[#13141C]">
              <span className="text-[10px] uppercase tracking-widest opacity-80 mb-1">Impact</span>
              <span className="text-sm md:text-base font-bold leading-tight uppercase">Strategic<br/>Auditor</span>
            </div>
          </div>

          {/* Main Visual Frame */}
          <div className="relative z-10 w-72 h-96 md:w-[440px] md:h-[540px] bg-gray-200 dark:bg-[#1E202B] rounded-3xl md:rounded-[60px] overflow-hidden border-2 border-white/5 shadow-[0_40px_100px_rgba(0,0,0,0.5)]">
             <img 
                src="./image/pic_owe2.jpg" 
                alt="Rudy Prasetiya" 
                className="w-full h-full object-cover filter grayscale hover:grayscale-0 transition-all duration-1000 scale-105 hover:scale-100"
              />
          </div>

          {/* Leadership Bubble - Middle Right */}
          <div className="absolute bottom-16 -right-10 md:top-1/3 md:-right-20 z-20">
            <div className="w-32 h-32 md:w-44 md:h-44 bg-[#4AB7C3] rounded-full flex flex-col items-center justify-center text-gray-900 shadow-2xl transform rotate-12 hover:rotate-0 transition-all duration-500 text-center border-4 border-[#13141C]">
              <span className="text-[10px] uppercase tracking-widest opacity-70 mb-1">Vision</span>
              <span className="text-sm md:text-lg font-black leading-tight uppercase tracking-tighter">Security<br/>Strategist</span>
            </div>
          </div>

          {/* Impact Typography Overlay */}
          <div className="absolute -bottom-12 md:bottom-12 left-0 md:-left-24 z-30 pointer-events-none">
            <h1 className="text-6xl md:text-8xl lg:text-9xl font-black text-gray-900 dark:text-white leading-[0.85] tracking-tighter drop-shadow-[0_20px_40px_rgba(0,0,0,0.5)]">
              Rudy <br className="hidden md:block"/>
              Prasetiya <span className="text-[#4AB7C3] inline-block animate-pulse">.</span>
            </h1>
          </div>
        </div>

        {/* Executive Info Column */}
        <div className="col-span-1 md:col-span-5 mt-20 md:mt-32 px-4 md:pl-10 relative z-40">
          <div className="max-w-md">
            <p className="text-[10px] font-bold uppercase tracking-[0.5em] text-[#4AB7C3] mb-4">/ Executive Profile</p>
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
              Directing the intersection of <span className="italic font-serif">Governance</span>, <span className="italic font-serif">Policy</span>, and <span className="italic font-serif">Security</span>.
            </h2>
            
            <div className="space-y-4 text-gray-600 dark:text-gray-400 text-sm md:text-base leading-relaxed mb-8">
              <p>
                As an <strong>IT Auditor & Cybersecurity Leader</strong>, I don’t just find vulnerabilities—I build organizational resilience. My focus is the strategic alignment of IT GRC, Risk & Compliance, and Sustainability Policy.
              </p>
              <div className="pt-4 border-l-2 border-[#5D5CDE] pl-4">
                <p className="text-xs uppercase tracking-widest text-gray-500 mb-1">Credentialed Excellence</p>
                <p className="font-bold text-gray-900 dark:text-gray-200">SST, MA, MSE, CDSP, CC</p>
              </div>
              <div className="pt-2 border-l-2 border-[#4AB7C3] pl-4">
                <p className="text-xs uppercase tracking-widest text-gray-500 mb-1">Academic Foundation</p>
                <p className="text-xs leading-snug">
                  MA Int'l Development (IUJ Japan) &<br/>
                  MSE Economics (University of Indonesia)
                </p>
              </div>
            </div>
            
            <a href="#contact" className="inline-flex items-center gap-4 text-xs font-bold uppercase tracking-widest text-gray-900 dark:text-white group">
              Start a strategic conversation
              <span className="w-10 h-10 rounded-full border border-gray-700 flex items-center justify-center group-hover:bg-[#4AB7C3] group-hover:border-[#4AB7C3] group-hover:text-gray-900 transition-all duration-300">
                →
              </span>
            </a>
          </div>
        </div>
      </div>

      {/* Strategic Pillars Row */}
      <div className="mt-32 md:mt-48 grid grid-cols-1 md:grid-cols-3 gap-12 border-t border-gray-200 dark:border-gray-800 pt-16">
        
        {/* Pillar 1 */}
        <div className="relative group">
           <span className="text-[120px] md:text-[160px] font-black text-gray-200 dark:text-white/5 absolute -top-16 -left-4 -z-10 select-none group-hover:text-[#4AB7C3]/10 transition-colors">01</span>
           <div className="relative z-10">
             <h4 className="text-xs font-bold uppercase tracking-[0.3em] text-[#4AB7C3] mb-3">Audit Excellence</h4>
             <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">7+ Years of Governance</h3>
             <p className="text-sm text-gray-500 leading-relaxed">Systematic oversight in financial public management, ensuring integrity in multi-million dollar fiscal architectures.</p>
           </div>
        </div>

        {/* Pillar 2 */}
        <div className="relative group">
           <span className="text-[120px] md:text-[160px] font-black text-gray-200 dark:text-white/5 absolute -top-16 -left-4 -z-10 select-none group-hover:text-[#5D5CDE]/10 transition-colors">02</span>
           <div className="relative z-10">
             <h4 className="text-xs font-bold uppercase tracking-[0.3em] text-[#5D5CDE] mb-3">Security Risk</h4>
             <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">100% Resilience Focus</h3>
             <p className="text-sm text-gray-500 leading-relaxed">Developing cybersecurity roadmaps that balance strict compliance (NIST) with operational agility and growth.</p>
           </div>
        </div>

        {/* Global Impact */}
        <div className="flex flex-col justify-end">
            <h4 className="text-xs font-bold uppercase tracking-[0.3em] text-gray-500 mb-6">Global Standards</h4>
            <div className="flex flex-wrap items-center gap-8 opacity-40 grayscale hover:grayscale-0 transition-all duration-700">
               <span className="text-xl font-black tracking-tighter">ISACA</span>
               <span className="text-xl font-black tracking-tighter">ISC2</span>
               <span className="text-xl font-black tracking-tighter">IIA</span>
            </div>
            <p className="mt-6 text-[10px] text-gray-500 uppercase tracking-widest font-bold">Adhering to world-class security & audit benchmarks.</p>
        </div>

      </div>
    </section>
  );
};

export default IntroSection;
