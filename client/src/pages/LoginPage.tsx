import React, { useState } from 'react';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import './Auth.css';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle login logic here
    console.log({ email, password });
  };

  return (
    <div className="auth-page">
      <Card className="auth-card">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" variant="primary">Login</Button>
        </form>
        <div className="auth-links">
          <a href="/signup">Don't have an account? Sign Up</a>
          <a href="/forgot-password">Forgot Password?</a>
        </div>
      </Card>
    </div>
  );
};

export default LoginPage;
