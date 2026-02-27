
import React, { useState, useRef } from 'react';
import { FEATURED_PROJECTS } from '../constants';
import type { FeaturedProject } from '../types';

const FeaturedProjectCard: React.FC<{ project: FeaturedProject; index: number }> = ({ project, index }) => {
  const isLarge = index === 0;
  const cardRef = useRef<HTMLDivElement>(null);
  const [offset, setOffset] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLAnchorElement>) => {
    if (!cardRef.current) return;

    const { left, top, width, height } = cardRef.current.getBoundingClientRect();
    const x = (e.clientX - left) / width;
    const y = (e.clientY - top) / height;

    // Calculate translation (max 15px movement in any direction)
    const moveX = (x - 0.5) * 30;
    const moveY = (y - 0.5) * 30;

    setOffset({ x: moveX, y: moveY });
  };

  const handleMouseLeave = () => {
    setOffset({ x: 0, y: 0 });
  };
  
  return (
    <a 
      href={project.link} 
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className={`block group relative overflow-hidden rounded-[2.5rem] ${isLarge ? 'md:col-span-2 md:row-span-2 min-h-[450px]' : 'col-span-1 min-h-[280px]'}`}
    >
      <div 
        ref={cardRef}
        className={`w-full h-full relative bg-white dark:bg-[#1E202B] hover:bg-gray-50 dark:hover:bg-[#252836] transition-all duration-700 border border-gray-200 dark:border-white/5 hover:border-gray-300 dark:hover:border-white/10 group-hover:shadow-[0_40px_80px_rgba(0,0,0,0.3)]`}
      >
        {/* Content Container */}
        <div className="absolute inset-0 z-10 p-10 flex flex-col justify-between">
          <div className="flex justify-between items-start">
             <div className="h-12 w-px bg-[#4AB7C3] transform group-hover:scale-y-150 transition-transform duration-500"></div>
             <span className={`inline-block px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest shadow-lg ${index % 2 === 0 ? 'bg-[#5D5CDE] text-white' : 'bg-[#4AB7C3] text-gray-900'}`}>
                {index === 0 ? 'Lead Engagement' : 'Strategic Case'}
             </span>
          </div>
          
          <div className="max-w-xs">
             <h3 className="text-2xl md:text-3xl font-black text-gray-900 dark:text-white mb-4 group-hover:-translate-y-2 transition-transform duration-500 leading-tight tracking-tight">
                {project.title}
             </h3>
             <div className="flex items-center gap-3 text-xs font-bold uppercase tracking-widest text-gray-500 dark:text-gray-400">
                Explore Strategy <span className="text-xl transition-transform duration-500 group-hover:translate-x-3 text-[#4AB7C3]">→</span>
             </div>
          </div>
        </div>

        {/* Technical Background Aesthetic with Parallax */}
        <div 
          className="absolute inset-0 opacity-10 dark:opacity-30 group-hover:opacity-20 dark:group-hover:opacity-40 transition-opacity duration-700 overflow-hidden"
        >
           <img 
              src={project.imageUrl} 
              alt={project.title} 
              style={{
                transform: `scale(1.15) translate(${offset.x}px, ${offset.y}px)`,
                transition: offset.x === 0 ? 'transform 0.7s cubic-bezier(0.23, 1, 0.32, 1)' : 'none'
              }}
              className="w-full h-full object-cover grayscale transition-all duration-1000" 
            />
           {/* Abstract grid pattern overlay */}
           <div className="absolute inset-0 bg-[radial-gradient(#ffffff10_1px,transparent_1px)] [background-size:20px_20px]"></div>
           <div className="absolute inset-0 bg-gradient-to-t from-white via-white/80 to-transparent dark:from-[#13141C] dark:via-[#13141C]/80 dark:to-transparent"></div>
        </div>
      </div>
    </a>
  );
};

const FeaturedSection = (): React.ReactNode => {
  return (
    <section className="mb-32">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 gap-6">
        <div>
           <p className="text-[10px] font-black uppercase tracking-[0.5em] text-[#5D5CDE] mb-2">/ Portfolio</p>
           <h2 className="text-4xl md:text-5xl font-black text-gray-900 dark:text-white tracking-tighter italic font-serif">Strategic Engagements.</h2>
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-500">
           <span className="font-bold text-gray-900 dark:text-gray-300">2024—2026</span>
           <div className="h-px w-20 bg-gray-700"></div>
           <span className="uppercase tracking-widest text-[10px]">Oversight Portfolio</span>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-8 auto-rows-fr">
        {FEATURED_PROJECTS.map((project, index) => (
          <FeaturedProjectCard key={project.id} project={project} index={index} />
        ))}
        
        <div className="bg-transparent rounded-[2.5rem] p-10 flex flex-col justify-end border-2 border-dashed border-gray-200 dark:border-gray-800 text-gray-400 dark:text-gray-500 hover:border-gray-400 dark:hover:border-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-all duration-500 cursor-pointer min-h-[280px] group">
           <div className="text-4xl mb-4 group-hover:rotate-45 transition-transform duration-500">↗</div>
           <h4 className="text-sm font-bold uppercase tracking-widest">Full Archive</h4>
           <p className="text-xs opacity-60">View all historical governance engagements</p>
        </div>
      </div>
    </section>
  );
};

export default FeaturedSection;
