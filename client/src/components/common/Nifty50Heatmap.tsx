import React, { useState, useEffect } from 'react';
import './Nifty50Heatmap.css';

interface Stock {
  symbol: string;
  price: number;
  change_percent: number;
}

const Nifty50Heatmap: React.FC = () => {
  const [data, setData] = useState<Stock[]>([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/nifty50');

    ws.onmessage = (event) => {
      const stock = JSON.parse(event.data);
      setData((prevData) => {
        const existingStockIndex = prevData.findIndex((s) => s.symbol === stock.symbol);
        if (existingStockIndex !== -1) {
          const newData = [...prevData];
          newData[existingStockIndex] = stock;
          return newData;
        } else {
          return [...prevData, stock];
        }
      });
    };

    return () => {
      ws.close();
    };
  }, []);

  const getColor = (change: number) => {
    if (change > 0) {
      return `rgba(0, 255, 0, ${Math.min(change / 2, 1)})`;
    } else {
      return `rgba(255, 0, 0, ${Math.min(Math.abs(change) / 2, 1)})`;
    }
  };

  return (
    <div className="nifty50-heatmap">
      {data.map((stock) => (
        <div
          key={stock.symbol}
          className="heatmap-cell"
          style={{ backgroundColor: getColor(stock.change_percent) }}
        >
          <div className="symbol">{stock.symbol}</div>
          <div className="change">{stock.change_percent.toFixed(2)}%</div>
        </div>
      ))}
    </div>
  );
};

export default Nifty50Heatmap;
