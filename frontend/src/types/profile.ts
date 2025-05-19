import { User } from './user';

export interface Profile {
    id: number;
    avatar: string;
    bio: string;
    user: User;
}