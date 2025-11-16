import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import Button from '../components/common/Button';
import './Table.css';

const LogsAndAlertsPage: React.FC = () => {
  const logs = [
    { id: 1, type: 'INFO', message: 'Strategy started', timestamp: '2024-07-29 10:00:00' },
    { id: 2, type: 'ERROR', message: 'Upstox connection failed', timestamp: '2024-07-29 10:05:00' },
    { id: 3, type: 'TRADE', message: 'BUY INFY @ 1500', timestamp: '2024-07-29 10:10:00' },
  ];

  return (
    <MainLayout>
      <div className="page-container">
        <h2>Logs & Alerts</h2>
        <div className="actions">
          <Button>Download Logs</Button>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Log ID</th>
              <th>Type</th>
              <th>Message</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.type}</td>
                <td>{log.message}</td>
                <td>{log.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </MainLayout>
  );
};

export default LogsAndAlertsPage;
