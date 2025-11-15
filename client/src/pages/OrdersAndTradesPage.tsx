import React, { useState, useEffect } from 'react';
import MainLayout from '../components/layout/MainLayout';
import Button from '../components/common/Button';
import './Table.css';

interface Order {
  id: number;
  status: string;
  symbol: string;
  side: string;
  size: number;
  price: number;
  timestamp: string;
}

const OrdersAndTradesPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    fetch('/api/orders')
      .then(res => res.json())
      .then(data => setOrders(data));
  }, []);

  return (
    <MainLayout>
      <div className="page-container">
        <h2>Orders & Trades</h2>
        <div className="actions">
          <Button>Export CSV</Button>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Status</th>
              <th>Symbol</th>
              <th>Side</th>
              <th>Size</th>
              <th>Price</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>{order.status}</td>
                <td>{order.symbol}</td>
                <td>{order.side}</td>
                <td>{order.size}</td>
                <td>{order.price}</td>
                <td>{order.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </MainLayout>
  );
};

export default OrdersAndTradesPage;
