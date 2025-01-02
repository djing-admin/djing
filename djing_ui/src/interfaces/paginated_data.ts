import { Field } from "@/interfaces/field";

export interface PaginatedData {
  per_page: number;
  page: number;
  start_record: number;
  end_record: number;
  count: number;
  num_pages: number;
  items: [Field]
  keys: {
    page_key: string;
    page_value: any;
    per_page_key: string;
    per_page_value: any;
    search_key: string;
    search_value: any;
    sort_direction_key: string;
    sort_direction_value: any;
    sort_order_key: string;
    sort_order_value: any;

  }
}