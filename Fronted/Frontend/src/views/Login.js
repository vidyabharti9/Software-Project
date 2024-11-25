import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../components/authContext'; // Add this import
import './Register.css'; // Assuming using the same CSS for simplicity

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const { login } = useContext(AuthContext);
  
    const handleLogin = async (e) => {
      e.preventDefault();
      console.log('Logging in with', email, password);
      // Send login data to the backend using Axios
      try {
        const response = await axios.post('http://localhost:8000/login', {
          email,
          password
        });
        if (response.status === 200) {
          // Handle successful login, e.g., save user details and navigate to dashboard
          console.log('Login successful:', response.data);
          // Save the user details in local storage or state management for further use
          localStorage.setItem('user', JSON.stringify(response.data));
          login(); // Update context
          navigate('/profile'); // Redirect to user dashboard
          window.location.reload(); // Force a hard reload
        } else {
          alert('Login failed');
        }
      } catch (error) {
        console.error('Error during login:', error);
        alert('Invalid email or password');
      }
    };
  
    return (
      <div className="container">
        <form onSubmit={handleLogin}>
          <h2 className="head">Login</h2>
          <div>
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    );
  };
  
  export default Login;
