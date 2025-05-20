import { Category } from './category';

export interface Product {
    id: number;
    image: string;
    name: string;
    slug: string;
    price: number;
    description: string;
    category: Category;
    stock: number;
}