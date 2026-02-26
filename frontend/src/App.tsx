
import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import RightBentoPanel from './components/RightBentoPanel';
import './App.css';

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [rightPanelCollapsed, setRightPanelCollapsed] = useState(false);

  return (
    <div className="bg-brand-dark text-gray-200 font-sans min-h-screen flex transition-colors duration-300 overflow-hidden">
      {/* 1:4:1 Ratio Layout Implementation - Mobile Responsive */}
      <div className="hidden md:block h-full">
        <Sidebar collapsed={sidebarCollapsed} setCollapsed={setSidebarCollapsed} />
      </div>

      <main className="flex-grow flex flex-col h-screen overflow-hidden border-x border-white/5 bg-brand-panel/50 backdrop-blur-sm relative">
        <ChatInterface />
      </main>

      <div className="hidden xl:block h-full shrink-0 transition-all duration-300">
        <RightBentoPanel collapsed={rightPanelCollapsed} setCollapsed={setRightPanelCollapsed} />
      </div>
    </div>
  );
}

export default App;
