
import React from 'react';
import ThemeToggleButton from './ThemeToggleButton';

const Header = (): React.ReactNode => {
  return (
    <header className="w-full py-8 text-gray-400">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center">
        <div className="flex space-x-6 text-sm font-medium tracking-wide mb-4 md:mb-0">
          <a href="#" className="hover:text-white transition-colors">Stories.</a>
          <a href="#" className="hover:text-white transition-colors">Works.</a>
          <a href="#" className="hover:text-white transition-colors">Contacts.</a>
        </div>
        
        <div className="flex items-center space-x-6">
          <div className="text-white font-bold tracking-widest uppercase text-sm">
            RUDY / P.
          </div>
          <ThemeToggleButton />
        </div>
      </div>
    </header>
  );
};

export default Header;
