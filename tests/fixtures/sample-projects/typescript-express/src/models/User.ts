export interface IUser {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
}

export class User implements IUser {
  constructor(
    public id: string,
    public email: string,
    public name: string | undefined,
    public createdAt: Date
  ) {}

  validate(): boolean {
    return this.email.includes('@');
  }

  toJSON(): object {
    return {
      id: this.id,
      email: this.email,
      name: this.name,
      createdAt: this.createdAt.toISOString()
    };
  }
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
