import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import './Form.css';

const SettingsPage: React.FC = () => {
  return (
    <MainLayout>
      <div className="page-container">
        <h2>Settings</h2>
        <Card>
          <h3>Profile Settings</h3>
          {/* Profile settings form will go here */}
        </Card>
        <Card>
          <h3>Risk Management</h3>
          <div className="form-group">
            <label htmlFor="max-capital">Max Capital</label>
            <input type="number" id="max-capital" />
          </div>
          <div className="form-group">
            <label htmlFor="max-trades">Max Trades per Day</label>
            <input type="number" id="max-trades" />
          </div>
          <Button>Save Settings</Button>
        </Card>
        <Card>
          <h3>Notifications</h3>
          {/* Notification settings form will go here */}
        </Card>
      </div>
    </MainLayout>
  );
};

export default SettingsPage;
