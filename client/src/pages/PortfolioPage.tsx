import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import Card from '../components/common/Card';
import './PortfolioPage.css';

const PortfolioPage: React.FC = () => {
  return (
    <MainLayout>
      <div className="portfolio-page">
        <h2>Portfolio</h2>
        <div className="portfolio-summary">
          <Card>
            <h3>Holdings</h3>
            <p>₹1,00,000</p>
          </Card>
          <Card>
            <h3>Positions</h3>
            <p>₹23,456</p>
          </Card>
          <Card>
            <h3>Unrealised PnL</h3>
            <p>+₹5,678</p>
          </Card>
          <Card>
            <h3>Realised PnL</h3>
            <p>+₹1,234</p>
          </Card>
        </div>
        <div className="portfolio-charts">
          <Card>
            <h3>Day-wise PnL</h3>
            {/* Chart will go here */}
          </Card>
          <Card>
            <h3>Sector-wise Allocation</h3>
            {/* Chart will go here */}
          </Card>
        </div>
      </div>
    </MainLayout>
  );
};

export default PortfolioPage;
