import React, { useState } from 'react';
import MainLayout from '../components/layout/MainLayout';
import Button from '../components/common/Button';
import './StrategyBuilderPage.css';

const StrategyBuilderPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('no-code');

  return (
    <MainLayout>
      <div className="strategy-builder-page">
        <div className="tabs">
          <button
            className={activeTab === 'no-code' ? 'active' : ''}
            onClick={() => setActiveTab('no-code')}
          >
            No-Code Builder
          </button>
          <button
            className={activeTab === 'code-editor' ? 'active' : ''}
            onClick={() => setActiveTab('code-editor')}
          >
            Code Editor
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'no-code' && (
            <div className="no-code-builder">
              {/* No-code builder UI will go here */}
              <h3>No-Code Builder</h3>
              <p>Drag and drop blocks to build your strategy.</p>
            </div>
          )}
          {activeTab === 'code-editor' && (
            <div className="code-editor">
              {/* Code editor UI will go here */}
              <h3>Code Editor</h3>
              <textarea className="code-textarea" />
              <Button>Backtest</Button>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default StrategyBuilderPage;
