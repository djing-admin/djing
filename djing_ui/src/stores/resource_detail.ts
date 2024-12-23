import { defineStore } from "pinia";

type RootState = {
  loading: boolean,
  data: Record<string, any>;
};

export const useResourceDetailStore = defineStore({
  id: "resourceDetailStore",
  state: (): RootState => ({
    loading: false,
    data: {
      cards: [],
      panels: [],
      actions: [],
      title: null,
      resource: {},
    },
  }),
  actions: {
    update_data(key: string, value: any) {
      this.data[key] = value
    },

    reset_data() {
      this.data = {
        cards: [],
        panels: [],
        actions: [],
        title: null,
        resource: {},
      }
    },

    reset() {
      this.reset_data()
    }
  },
});