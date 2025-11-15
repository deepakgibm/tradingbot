import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import './MarketDataPage.css';

const MarketDataPage: React.FC = () => {
  return (
    <MainLayout>
      <div className="market-data-page">
        <aside className="filters-sidebar">
          <h3>Filters</h3>
          {/* Filter options will go here */}
        </aside>
        <main className="chart-container">
          {/* Candlestick chart will go here */}
          <h3>Market Chart</h3>
        </main>
      </div>
    </MainLayout>
  );
};

export default MarketDataPage;
