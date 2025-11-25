import express, { Request, Response } from 'express';
import { User } from '../models/User';
import { AuthService } from '../services/AuthService';

const router = express.Router();
const authService = new AuthService();

router.post('/login', async (req: Request, res: Response) => {
  const { email, password } = req.body;

  try {
    const token = await authService.login(email, password);
    res.json({ token, success: true });
  } catch (error) {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

router.post('/register', async (req: Request, res: Response) => {
  const { email, password, name } = req.body;

  try {
    const user = await authService.register(email, password, name);
    res.status(201).json({ user, success: true });
  } catch (error) {
    res.status(400).json({ error: 'Registration failed' });
  }
});

router.get('/profile', async (req: Request, res: Response) => {
  const userId = req.headers['x-user-id'] as string;

  try {
    const user = await authService.getProfile(userId);
    res.json({ user });
  } catch (error) {
    res.status(404).json({ error: 'User not found' });
  }
});

export default router;
