import { defineStore } from "pinia";

type RootState = {
  loading: boolean,
  form: Record<string, any>;
  data: Record<string, any>;
};

export const useResourceFormStore = defineStore({
  id: "resourceFormStore",
  state: (): RootState => ({
    loading: false,
    form: {
      is_dirty: false,
      loading: false,
      data: {},
      errors: {}
    },
    data: {
      title: null,
      fields: [],
      panels: [],
    },
  }),
  getters: {
    form_data(state: any) {
      return state.form.data
    }
  },
  actions: {
    update_data(key: string, value: any) {
      this.data[key] = value
    },

    reset_data() {
      this.data = {
        title: null,
        fields: [],
        panels: [],
      }
    },

    get_field_default_value(field: any) {
      if (this.form.data.hasOwnProperty(field.attribute)) {
        return this.form.data[field.attribute]
      }

      this.form.data[field.attribute] = field.value

      return this.form.data[field.attribute]
    },

    reset_form() {
      this.form = {
        is_dirty: false,
        loading: false,
        data: {},
        errors: {}
      }
    },

    set_form_data(key: any, value: any) {
      this.form.data[key] = value
    },

    set_form_is_dirty(is_dirty: boolean) {
      this.form.is_dirty = is_dirty
    },

    set_form_errors(errors: any) {
      this.form.errors = errors
    },

    reset() {
      this.reset_data()
      this.reset_form()
    }
  },
});