import { User } from "./user";
import { ProductGroup } from "./productgroup";
export interface Recipe {
    id: number;
    name: string;
    slug: string;
    description: string;
    created_at: string;
    updated_at: string;
    user: User;
    product_group: ProductGroup;
}