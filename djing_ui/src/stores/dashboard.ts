import { defineStore } from "pinia";

type RootState = {
  loading: boolean,
  data: Record<string, any>;
};

export const useDashboardStore = defineStore({
  id: "dashboardStore",
  state: (): RootState => ({
    loading: false,
    data: {
      label: "",
      cards: [],
      show_refresh_button: false,
      is_help_card: false
    },
  }),
  actions: {
    update_data(key: string, value: any) {
      this.data[key] = value
    },

    reset_data() {
      this.data = {
        label: "",
        cards: [],
        show_refresh_button: false,
        is_help_card: false
      }
    },

    reset() {
      this.reset_data()
    }
  },
});