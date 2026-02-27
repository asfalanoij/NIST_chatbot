
import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import RightBentoPanel from './components/RightBentoPanel';

function App(): React.ReactNode {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [rightPanelCollapsed, setRightPanelCollapsed] = useState(false);

  return (
    <div className="bg-[#0B0C10] text-gray-200 font-sans min-h-screen flex transition-colors duration-300 overflow-hidden">
      {/* 1:4:1 Ratio Layout Implementation */}
      <Sidebar collapsed={sidebarCollapsed} setCollapsed={setSidebarCollapsed} />
      
      <main className="flex-grow flex flex-col h-screen overflow-hidden border-x border-white/5 bg-[#13141C]/50 backdrop-blur-sm">
        <ChatInterface />
      </main>

      <RightBentoPanel collapsed={rightPanelCollapsed} setCollapsed={setRightPanelCollapsed} />
    </div>
  );
}

export default App;
