import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css'; // Make sure this path is correct
import axios from 'axios';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [username, setUsername] = useState('');
  const [userDetails, setUserDetails] = useState('');
  const [subDetails, setSubDetails] = useState('');
  const [profession, setProfession] = useState('');
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    console.log('Registering with', email, password, username, userDetails, subDetails, profession);

    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('username', username);
    formData.append('user_details', userDetails);
    formData.append('sub_details', subDetails);
    formData.append('profession', profession);
    if (image) {
      formData.append('image', image);
    }

    // Send registration data to the backend using Axios
    try {
      const response = await axios.post('http://localhost:8000/register', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status === 200) {
        navigate('/login');
      } else {
        alert('Registration failed');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      alert('An error occurred during registration');
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleRegister}>
        <h2 className="head">Register</h2>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <div>
          <label>Confirm Password:</label>
          <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
        </div>
        <div>
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div>
          <label>User Details:</label>
          <textarea value={userDetails} onChange={(e) => setUserDetails(e.target.value)} required></textarea>
        </div>
        <div>
          <label>Sub Details:</label>
          <textarea value={subDetails} onChange={(e) => setSubDetails(e.target.value)} required></textarea>
        </div>
        <div>
          <label>Profession:</label>
          <input type="text" value={profession} onChange={(e) => setProfession(e.target.value)} required />
        </div>
        <div>
          <label>Profile Image:</label>
          <input type="file" onChange={(e) => setImage(e.target.files[0])} />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
