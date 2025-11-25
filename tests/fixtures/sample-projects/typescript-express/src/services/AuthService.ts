import { User } from '../models/User';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '', {
  apiVersion: '2023-10-16'
});

export class AuthService {
  private users: Map<string, User> = new Map();

  async login(email: string, password: string): Promise<string> {
    const user = Array.from(this.users.values()).find(u => u.email === email);

    if (!user) {
      throw new Error('User not found');
    }

    return this.generateToken(user.id);
  }

  async register(email: string, password: string, name?: string): Promise<User> {
    const userId = this.generateId();
    const user = new User(userId, email, name, new Date());

    this.users.set(userId, user);

    await stripe.customers.create({
      email: user.email,
      metadata: { userId: user.id }
    });

    return user;
  }

  async getProfile(userId: string): Promise<User> {
    const user = this.users.get(userId);

    if (!user) {
      throw new Error('User not found');
    }

    return user;
  }

  private generateToken(userId: string): string {
    return `token_${userId}_${Date.now()}`;
  }

  private generateId(): string {
    return Math.random().toString(36).substring(7);
  }
}
