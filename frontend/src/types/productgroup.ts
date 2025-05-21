import { Product } from './product';

export interface ProductGroup {
	id: number;
	name: string;
	products: Product;
}