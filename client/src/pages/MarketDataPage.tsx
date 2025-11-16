import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import MainLayout from '../components/layout/MainLayout';
import './MarketDataPage.css';

const MarketDataPage: React.FC = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Replace with a real instrument key
    fetch('/api/historical-data/NSE_EQ|INE848E01016')
      .then(res => res.json())
      .then(data => {
        const formattedData = data.map((d: any) => ({
          name: new Date(d[0]).toLocaleTimeString(),
          open: d[1],
          high: d[2],
          low: d[3],
          close: d[4],
        }));
        setData(formattedData);
      });
  }, []);

  return (
    <MainLayout>
      <div className="market-data-page">
        <aside className="filters-sidebar">
          <h3>Filters</h3>
          {/* Filter options will go here */}
        </aside>
        <main className="chart-container">
          <h3>Market Chart</h3>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="open" stroke="#8884d8" />
              <Line type="monotone" dataKey="high" stroke="#82ca9d" />
              <Line type="monotone" dataKey="low" stroke="#ffc658" />
              <Line type="monotone" dataKey="close" stroke="#ff7300" />
            </LineChart>
          </ResponsiveContainer>
        </main>
      </div>
    </MainLayout>
  );
};

export default MarketDataPage;
