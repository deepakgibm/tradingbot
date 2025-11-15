import React, { useContext } from 'react';
import { ThemeContext } from '../../context/ThemeContext';
import Button from './Button';

const ThemeSwitcher: React.FC = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <Button onClick={toggleTheme}>
      Switch to {theme === 'light' ? 'Dark' : 'Light'} Mode
    </Button>
  );
};

export default ThemeSwitcher;
