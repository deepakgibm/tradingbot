import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import './Form.css';

const UpstoxIntegrationPage: React.FC = () => {
  return (
    <MainLayout>
      <div className="page-container">
        <h2>Upstox Integration</h2>
        <Card>
          <div className="form-group">
            <label htmlFor="api-key">API Key</label>
            <input type="text" id="api-key" />
          </div>
          <div className="form-group">
            <label htmlFor="webhook-url">Webhook URL</label>
            <input type="text" id="webhook-url" readOnly value="https://your-app.com/webhook" />
          </div>
          <Button>Connect to Upstox</Button>
        </Card>
      </div>
    </MainLayout>
  );
};

export default UpstoxIntegrationPage;
