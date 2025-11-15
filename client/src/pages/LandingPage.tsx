import React from 'react';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  return (
    <div className="landing-page">
      <header className="hero-section">
        <h1>Automated Algo Trading for the Indian Market using Upstox API</h1>
        <Button variant="primary">Connect Upstox</Button>
      </header>

      <main>
        <section className="features-section">
          <h2>Features</h2>
          <div className="features-grid">
            <Card>
              <h3>Algo Trading</h3>
              <p>Automate your trading strategies with our powerful and flexible platform.</p>
            </Card>
            <Card>
              <h3>Backtesting</h3>
              <p>Test your strategies against historical data to optimize your performance.</p>
            </Card>
            <Card>
              <h3>Real-time Data</h3>
              <p>Get access to live market data from Upstox to make informed decisions.</p>
            </Card>
            <Card>
              <h3>AI Strategies</h3>
              <p>Leverage our AI-powered strategies to gain an edge in the market.</p>
            </Card>
          </div>
        </section>

        <section className="pricing-section">
          <h2>Pricing</h2>
          <div className="pricing-grid">
            <Card>
              <h3>Monthly</h3>
              <p className="price">$49/month</p>
              <Button>Choose Plan</Button>
            </Card>
            <Card>
              <h3>Yearly</h3>
              <p className="price">$499/year</p>
              <Button>Choose Plan</Button>
            </Card>
          </div>
        </section>

        <section className="testimonials-section">
          <h2>Testimonials</h2>
          <div className="testimonials-grid">
            <Card>
              <p>"This is the best trading platform I have ever used. The AI strategies are a game-changer."</p>
              <p className="author">- John Doe</p>
            </Card>
            <Card>
              <p>"The backtesting engine is incredibly fast and accurate. I was able to optimize my strategy in no time."</p>
              <p className="author">- Jane Smith</p>
            </Card>
          </div>
        </section>
      </main>

      <footer className="footer-section">
        <div className="footer-links">
          <a href="/support">Support</a>
          <a href="/docs">Docs</a>
          <a href="/privacy">Privacy</a>
        </div>
        <p>&copy; 2024 AI Trading Bot. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
