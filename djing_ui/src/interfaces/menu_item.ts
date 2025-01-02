import { Badge } from "@/interfaces/badge";

export interface MenuItem {
  component: string;
  name: string;
  badge: Badge;
  icon: string;
  path: string;
  collapsable: boolean;
  active: boolean;
}