import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import MainLayout from '../components/layout/MainLayout';
import Nifty50Heatmap from '../components/common/Nifty50Heatmap';
import './DashboardPage.css';

interface Portfolio {
  total_account_balance: number;
  todays_pnl: number;
  monthly_pnl: number;
  active_strategies: number;
}

const DashboardPage: React.FC = () => {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);

  useEffect(() => {
    fetch('/api/portfolio')
      .then(res => res.json())
      .then(data => setPortfolio(data));
  }, []);

  return (
    <MainLayout>
      <div className="dashboard-page">
        <div className="overview-cards">
          <Card>
            <h3>Total Account Balance</h3>
            <p>{portfolio ? `₹${portfolio.total_account_balance.toLocaleString()}` : 'Loading...'}</p>
          </Card>
          <Card>
            <h3>Today's PnL</h3>
            <p>{portfolio ? `₹${portfolio.todays_pnl.toLocaleString()}` : 'Loading...'}</p>
          </Card>
          <Card>
            <h3>Monthly PnL</h3>
            <p>{portfolio ? `₹${portfolio.monthly_pnl.toLocaleString()}` : 'Loading...'}</p>
          </Card>
          <Card>
            <h3>Active Strategies</h3>
            <p>{portfolio ? portfolio.active_strategies : 'Loading...'}</p>
          </Card>
        </div>

        <div className="ticker">
          <p>NIFTY: 18,234.56 (+0.5%)</p>
          <p>BANKNIFTY: 42,345.67 (+0.8%)</p>
          <p>FINNIFTY: 19,876.54 (+0.6%)</p>
        </div>

        <div className="notifications-panel">
          <h3>Notifications</h3>
          <ul>
            <li>[Signal] BUY INFY @ 1500</li>
            <li>[Error] Upstox connection failed</li>
            <li>[Fill] SELL RELIANCE @ 2500</li>
          </ul>
        </div>

        <div className="heatmap-container">
          <h3>Nifty 50 Heatmap</h3>
          <Nifty50Heatmap />
        </div>
      </div>
    </MainLayout>
  );
};

export default DashboardPage;
