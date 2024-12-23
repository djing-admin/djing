import { filter } from "lodash";
import { defineStore } from "pinia";

type RootState = {
  loading: boolean,
  data: Record<string, any>;
  selected_resources: {
    all: boolean,
    ids: Array<number>
  };
  query: Record<string, any>;
};

export const useResourceIndexStore = defineStore({
  id: "resourceIndexStore",
  state: (): RootState => ({
    loading: false,
    data: {
      cards: [],
      lenses: [],
      filters: [],
      actions: [],
      pagination: {},
      resources: [],
      sortable: true
    },
    selected_resources: {
      all: false,
      ids: []
    },
    query: {
      search: "",
      filter: "",
      per_page: "",
      page: "",
      order_by: "",
      order_by_direction: ""
    }
  }),
  getters: {
    available_filters: (state) => {
      return Object.values(state.data.filters).map((filter: any) => {
        return { [filter.class]: filter.current_value };
      });
    },

    applied_filters: (state: any) => {
      return Object.values(state.data.filters).filter((filter: any) => {
        return JSON.stringify(filter.current_value) !== JSON.stringify(filter.default_value);
      });
    },

    all_selected(state: any): boolean {
      return state.selected_resources.all
    },

    page_selected(state: any): boolean {
      return state.data.resources.every((resource: any) => state.selected_resources.ids.includes(resource.id.value))
    },

    pick_selected(state: any): boolean {
      return state.selected_resources.ids.length > 0
    },

    total_selected_resources(state: any) {
      if (this.all_selected) {
        return state.data.pagination.total;
      }

      if (this.page_selected) {
        return state.selected_resources.ids.length;
      }

      if (this.pick_selected) {
        return state.selected_resources.ids.length;
      }

      return 0;
    },

    has_selected_resources(state: any) {
      const resources = filter(
        state.data.resources,
        (resource: any) => {
          return resource.authorized_to_delete;
        }
      );

      return resources.length > 0;
    },

    get_selected_resources(state: any) {
      return state.selected_resources.all
        ? "all"
        : state.selected_resources.ids.join(",");
    }
  },
  actions: {
    update_data(key: string, value: any) {
      this.data[key] = value
    },

    update_query(key: string, value: any) {
      this.query[key] = value
    },

    reset_query() {
      this.query = {
        search: "",
        filter: "",
        per_page: "",
        page: "",
        order_by: "",
        order_by_direction: ""
      }
    },

    reset_data() {
      this.reset_cards()
      this.reset_lenses()
      this.reset_filters()
      this.reset_actions()
      this.reset_resources()
    },

    reset_selected_resources() {
      this.selected_resources = {
        all: false,
        ids: []
      }
    },

    reset_cards() {
      this.data = {
        ...this.data,
        cards: [],
      }
    },

    reset_lenses() {
      this.data = {
        ...this.data,
        lenses: [],
      }
    },

    reset_filters() {
      this.data = {
        ...this.data,
        filters: [],
      }
    },

    reset_actions() {
      this.data = {
        ...this.data,
        actions: [],
      }
    },

    reset_resources() {
      this.data = {
        ...this.data,
        resources: [],
        pagination: {},
        sortable: true
      }
    },

    reset() {
      this.reset_query()
      this.reset_data()
      this.reset_selected_resources()
    }
  },
});