export interface Field {
  attribute: string;
  component: string;
  title: string;
  column: string;
  value: any;
  is_sortable: boolean;
  readonly: boolean;
  relationship_type?: string;
  fields?: Field[]
}