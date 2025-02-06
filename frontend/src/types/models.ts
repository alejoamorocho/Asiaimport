export interface Category {
  id: number;
  name: string;
  description: string;
  created_at?: string;
  updated_at?: string;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category_id: number;
  category_name?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Import {
  id: number;
  reference_number: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  import_date: string;
  documents: string | null;
  notes: string;
}

export interface ImportItem {
  id: number;
  import_record: Import;
  product: Product;
  expected_quantity: number;
  received_quantity: number;
  notes: string;
}

export interface ProductUnit {
  id: number;
  product: Product;
  import_item: ImportItem;
  serial_number: string;
  status: 'available' | 'in_use' | 'maintenance' | 'defective' | 'disposed';
  notes: string;
}
