import { defineStore } from "pinia";

type RootState = {
  resources: any;
  base: any;
  version: any;
  main_menu: any;
  main_menu_state: Record<string, any>,
  current_user: any;
  valid_license: any;
  breadcrumbs: any;
};

export const useDjingStore = defineStore({
  id: "djingStore",
  state: (): RootState => ({
    resources: null,
    base: null,
    version: null,
    main_menu: null,
    main_menu_state: {},
    current_user: null,
    valid_license: null,
    breadcrumbs: null,
  }),
  actions: {
    getMainMenuState(key: string): boolean {
      if (this.main_menu_state.hasOwnProperty(key)) {
        return this.main_menu_state[key]
      } else {
        return false
      }
    },
    toggleMainMenuState(key: string): void {
      this.main_menu_state[key] = !this.getMainMenuState(key)
    },
    assignPropsFromInertia(djing: any, page: any) {
      let config = page.props.djing_config || djing.appConfig

      let { resources, base, version, main_menu } = config

      let current_user = page.props.current_user

      let valid_license = page.props.valid_license

      let breadcrumbs = page.props.breadcrumbs || []

      djing.appConfig = config

      this.resources = resources

      this.base = base

      this.version = version

      this.main_menu = main_menu

      this.resources = resources

      this.current_user = current_user

      this.valid_license = valid_license

      this.breadcrumbs = breadcrumbs
    },
  },
  persist: {
    key: 'main_menu_state'
  },
});
