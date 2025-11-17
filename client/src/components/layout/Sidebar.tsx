import React from 'react';
import './Sidebar.css';

const Sidebar: React.FC = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>AI Trading Bot</h2>
      </div>
      <nav className="sidebar-nav">
        <ul>
          <li><a href="/dashboard">Dashboard</a></li>
          <li><a href="/strategy-builder">Strategy Builder</a></li>
          <li><a href="/market-data">Market Data</a></li>
          <li><a href="/orders">Orders & Trades</a></li>
          <li><a href="/portfolio">Portfolio</a></li>
          <li><a href="/upstox-integration">Upstox Integration</a></li>
          <li><a href="/logs">Logs & Alerts</a></li>
          <li><a href="/settings">Settings</a></li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
