import React, { useContext } from 'react';
import { ThemeProvider, ThemeContext } from './context/ThemeContext';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import DashboardPage from './pages/DashboardPage';
import StrategyBuilderPage from './pages/StrategyBuilderPage';
import MarketDataPage from './pages/MarketDataPage';
import OrdersAndTradesPage from './pages/OrdersAndTradesPage';
import PortfolioPage from './pages/PortfolioPage';
import UpstoxIntegrationPage from './pages/UpstoxIntegrationPage';
import LogsAndAlertsPage from './pages/LogsAndAlertsPage';
import SettingsPage from './pages/SettingsPage';
import TradingControlPage from './pages/TradingControlPage';
import ThemeSwitcher from './components/common/ThemeSwitcher';
import './dark-theme.css';

const App: React.FC = () => {
  const { theme } = useContext(ThemeContext);

  React.useEffect(() => {
    document.body.className = theme;
  }, [theme]);

  const route = window.location.pathname;

  const renderPage = () => {
    switch (route) {
      case '/login':
        return <LoginPage />;
      case '/signup':
        return <SignupPage />;
      case '/forgot-password':
        return <ForgotPasswordPage />;
      case '/dashboard':
        return <DashboardPage />;
      case '/strategy-builder':
        return <StrategyBuilderPage />;
      case '/market-data':
        return <MarketDataPage />;
      case '/orders':
        return <OrdersAndTradesPage />;
      case '/portfolio':
        return <PortfolioPage />;
      case '/upstox-integration':
        return <UpstoxIntegrationPage />;
      case '/logs':
        return <LogsAndAlertsPage />;
      case '/settings':
        return <SettingsPage />;
      case '/trading-control':
        return <TradingControlPage />;
      default:
        return <LandingPage />;
    }
  };

  return (
    <div>
      <ThemeSwitcher />
      {renderPage()}
    </div>
  );
};

const AppWrapper: React.FC = () => (
  <ThemeProvider>
    <App />
  </ThemeProvider>
);

export default AppWrapper;
