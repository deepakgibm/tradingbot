import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import './TradingControlPage.css';
import './Form.css';

const TradingControlPage: React.FC = () => {
  return (
    <MainLayout>
      <div className="trading-control-page">
        <h2>Trading Control</h2>
        <div className="control-cards-container">
          <Card className="control-card">
            <h3>AI Trading</h3>
            <div className="form-group">
              <label htmlFor="ai-algorithm">Select AI Trading Algorithm</label>
              <select id="ai-algorithm" className="form-control">
                <option>Momentum Master v1</option>
                <option>Mean Reversion Pro</option>
                <option>Volatility Skimmer</option>
              </select>
            </div>
            <div className="status-indicator">
              <span>Status: </span>
              <span className="status-stopped">Stopped</span>
            </div>
            <Button variant="primary">Start Trading</Button>
          </Card>

          <Card className="control-card">
            <h3>Manual Strategy</h3>
            <div className="form-group">
                <label>Entry Conditions</label>
                <textarea placeholder="e.g., EMA(20) > EMA(50) AND RSI < 30" className="form-control"></textarea>
            </div>
            <div className="form-group">
                <label>Exit Conditions</label>
                <textarea placeholder="e.g., RSI > 70 OR StopLoss" className="form-control"></textarea>
            </div>
             <div className="status-indicator">
              <span>Status: </span>
              <span className="status-stopped">Stopped</span>
            </div>
            <Button variant="primary">Start Manual Trading</Button>
          </Card>
        </div>
      </div>
    </MainLayout>
  );
};

export default TradingControlPage;

// Add a basic style for form-control in a shared css or here
// For now, extending Form.css in spirit
const styles = `
.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 5px;
}
`;
