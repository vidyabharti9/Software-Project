import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { AuthProvider } from './components/authContext'; // Add this import
import './style.css';
import Navbar from './components/navbar';
import Home from './views/home';
import DynamicForm from './views/Webanalyzer';
import Learn from './views/learn';
import UserDashboard from './views/user-dashboard';
import Login from './views/Login';
import Register from './views/Register';
import Maskgroup from './views/maskgroup';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/learn" element={<Learn />} />
          <Route path="/profile" element={<UserDashboard />} />
          <Route path="/analyzer" element={<DynamicForm />} />
          <Route path="/report" element={<Maskgroup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

ReactDOM.render(<App />, document.getElementById('app'));
