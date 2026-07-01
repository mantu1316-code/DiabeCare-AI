const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const nodemailer = require('nodemailer');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const User = require('./models/User');
const auth = require('./middleware/auth');

const app = express();
app.use(cors());
app.use(express.json());

// Rate limiting for OTP and login (Fixed syntax error)
const otpLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many requests from this IP, please try again after 15 minutes'
});

// Email transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
});

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

// ------------------- SIGNUP -------------------
app.post('/api/signup', async (req, res) => {
  try {
    const { name, email, phone, password } = req.body;
    const existing = await User.findOne({ $or: [{ email }, { phone }] });
    if (existing) return res.status(400).json({ message: 'Email or phone already registered' });
    
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const otpExpires = new Date(Date.now() + 10 * 60 * 1000); // 10 mins valid

    const user = new User({
      name,
      email,
      phone,
      password, // assuming pre-save hook hashes this
      otp,
      otpExpires,
      isVerified: false
    });

    await user.save();

    await transporter.sendMail({
      to: email,
      subject: 'Verify your Diabetes AI Account',
      html: `<p>Thank you for signing up. Your OTP for verification is <b>${otp}</b>. Valid for 10 minutes.</p>`
    });

    res.status(201).json({ message: 'User registered. OTP sent to email.' });
  } catch (err) {
    res.status(500).json({ message: 'Server error during signup' });
  }
});

// ------------------- VERIFY OTP (NEW ADDED ENDPOINT) -------------------
app.post('/api/verify-otp', async (req, res) => {
  try {
    const { email, otp } = req.body;
    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ message: 'User not found' });
    
    if (user.otp !== otp || user.otpExpires < new Date()) {
      return res.status(400).json({ message: 'Invalid or expired OTP' });
    }
    
    user.isVerified = true;
    user.otp = undefined;
    user.otpExpires = undefined;
    await user.save();
    
    res.json({ message: 'Email verified successfully!' });
  } catch (err) {
    res.status(500).json({ message: 'Server error during verification' });
  }
});

// ------------------- LOGIN -------------------
app.post('/api/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user) return res.status(400).json({ message: 'Invalid credentials' });
    
    if (!user.isVerified) {
      return res.status(401).json({ message: 'Please verify your email first.' });
    }

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(400).json({ message: 'Invalid credentials' });

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1d' });
    res.json({
      token,
      user: { id: user._id, name: user.name, email: user.email }
    });
  } catch (err) {
    res.status(500).json({ message: 'Server error during login' });
  }
});

// ------------------- FORGOT PASSWORD -------------------
app.post('/api/forgot-password', otpLimiter, async (req, res) => {
  const { email } = req.body;
  const user = await User.findOne({ email });
  if (!user) return res.status(404).json({ message: 'Email not registered' });
  
  const otp = Math.floor(100000 + Math.random() * 900000).toString();
  user.otp = otp;
  user.otpExpires = new Date(Date.now() + 10 * 60 * 1000);
  await user.save();
  
  await transporter.sendMail({
    to: email,
    subject: 'Reset your Diabetes AI password',
    html: `<p>Your OTP for password reset is <b>${otp}</b>. Valid for 10 minutes.</p>`
  });
  res.json({ message: 'OTP sent to your email' });
});

// ------------------- RESET PASSWORD -------------------
app.post('/api/reset-password', async (req, res) => {
  const { email, otp, newPassword } = req.body;
  const user = await User.findOne({ email });
  if (!user) return res.status(404).json({ message: 'User not found' });
  if (user.otp !== otp || user.otpExpires < new Date())
    return res.status(400).json({ message: 'Invalid or expired OTP' });
  
  user.password = newPassword; 
  user.otp = undefined;
  user.otpExpires = undefined;
  await user.save();
  
  res.json({ message: 'Password updated successfully' });
});

// ------------------- PORT CONFIG & START -------------------
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));