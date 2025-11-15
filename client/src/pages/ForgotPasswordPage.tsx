import React, { useState } from 'react';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import './Auth.css';

const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState('');

  const handleForgotPassword = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle forgot password logic here
    console.log({ email });
  };

  return (
    <div className="auth-page">
      <Card className="auth-card">
        <h2>Forgot Password</h2>
        <form onSubmit={handleForgotPassword}>
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
          <Button type="submit" variant="primary">Submit</Button>
        </form>
        <div className="auth-links">
          <a href="/login">Back to Login</a>
        </div>
      </Card>
    </div>
  );
};

export default ForgotPasswordPage;
