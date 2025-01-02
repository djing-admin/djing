import { Component, createApp, h } from "vue";
import { createInertiaApp, usePage } from "@inertiajs/vue3";
import "vite/modulepreload-polyfill";

import { createPinia } from "pinia";
import piniaPluginPersistedState from "pinia-plugin-persistedstate";

import { convertBrandColorsToCSSVariables } from "@/util/converter";
import { url } from "@/util/url";
import { setupAxios } from "@/util/axios";
import { registerFields, registerViews } from "@/components";

import Layout from "@/layouts/Layout.vue";
import isNil from "lodash/isNil";
import { TinyEmitter } from "tiny-emitter";
import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import { omit } from "lodash";
import { router } from "@inertiajs/vue3";
import { useDjingStore } from "@/stores/djing";
import Nprogress from "nprogress";
import Vue3Toastify, { type ToastContainerOptions, toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import localization from "@/mixins/localization";

export class Djing {
  appConfig: any;
  bootingCallbacks: any;
  mountTo: any;
  app: any;

  $progress: typeof Nprogress;
  $router: typeof router;
  $emitter: TinyEmitter;

  pages: Record<string, { default: Component }>;

  constructor(config: any) {
    this.appConfig = config;
    this.bootingCallbacks = [];
    this.mountTo = null;
    this.app = null;

    this.$progress = Nprogress;
    this.$router = router;
    this.$emitter = new TinyEmitter();

    const pages = import.meta.glob("./pages/**/*.vue", { eager: true }) as Record<string, { default: Component }>;

    this.pages = {
      "Djing.Test": pages["./pages/Test.vue"],
      "Djing.Attach": pages["./pages/Attach.vue"],
      "Djing.Create": pages["./pages/Create.vue"],
      "Djing.Dashboard": pages["./pages/Dashboard.vue"],
      "Djing.Detail": pages["./pages/Detail.vue"],
      "Djing.Error": pages["./pages/AppError.vue"],
      "Djing.Error403": pages["./pages/Error403.vue"],
      "Djing.Error404": pages["./pages/Error404.vue"],
      "Djing.ForgotPassword": pages["./pages/ForgotPassword.vue"],
      "Djing.Index": pages["./pages/Index.vue"],
      "Djing.Lens": pages["./pages/Lens.vue"],
      "Djing.Login": pages["./pages/Login.vue"],
      "Djing.Replicate": pages["./pages/Replicate.vue"],
      "Djing.ResetPassword": pages["./pages/ResetPassword.vue"],
      "Djing.Update": pages["./pages/Update.vue"],
      "Djing.UpdateAttached": pages["./pages/UpdateAttached.vue"],
    };
  }

  public booting(callback: any): void {
    this.bootingCallbacks.push(callback);
  }

  public boot(): void {
    this.bootingCallbacks.forEach((callback: any) => callback(this.app));
    this.bootingCallbacks = [];
  }

  public booted(callback: any): void {
    callback(this.app);
  }

  public config(key: string) {
    return this.appConfig[key];
  }

  public async countdown() {
    this.log("Initiating Djing countdown...");

    const appName = this.config("app_name");

    await createInertiaApp({
      title: (title) => (!title ? appName : `${title} - ${appName}`),
      resolve: (name): any => {
        const page: any = this.pages[name] || this.pages["Djing.Error404"];

        // Ensure layout is applied during the rendering setup.
        return {
          ...page,
          default: {
            ...page.default,
            layout: page.default.layout || Layout,
          },
        };
      },
      setup: ({ el, App, props, plugin }) => {
        this.mountTo = el;

        this.app = createApp({ render: () => h(App, props) });

        const pinia = createPinia();

        pinia.use(piniaPluginPersistedState);

        this.app
          .use(plugin)
          .use(pinia)
          .use(Vue3Toastify, {
            autoClose: 10000,
            theme: "colored",
          } as ToastContainerOptions);
      },
    });
  }

  public async liftOff() {
    this.log(`We have lift-off!`);

    registerViews(this);

    registerFields(this);

    this.boot();

    this.app.mixin(localization);

    this.$router.on("before", () => {
      this.assignPropsFromInertia();
    });

    this.$router.on("navigate", () => {
      this.assignPropsFromInertia();
    });

    this.app.mount(this.mountTo);

    this.applyTheme();

    this.log("All systems go...");
  }

  public assignPropsFromInertia() {
    const djingStore = useDjingStore();

    const page = usePage();

    djingStore.assignPropsFromInertia(this, page);
  }

  public inertia(name: string, component: any) {
    this.pages[name] = component;
  }

  public component(name: string, component: any) {
    if (isNil(this.app._context.components[name])) {
      this.app.component(name, component);
    }
  }

  info(message: string) {
    toast.info(message);
  }

  error(message: string) {
    toast.error(message);
  }

  success(message: string) {
    toast.success(message);
  }

  warning(message: string) {
    toast.warning(message);
  }

  public log(message: any) {
    console.log(`[DJING]`, message);
  }

  public applyTheme() {
    const rootStyles = convertBrandColorsToCSSVariables(this.config("brand_colors"));

    const styleElement = document.createElement("style");

    styleElement.textContent = rootStyles;

    document.head.appendChild(styleElement);
  }

  public url(path: string, parameters?: any) {
    if (path === "/") {
      path = this.config("initial_path");
    }

    return url(this.config("base"), path, parameters);
  }

  public request(options?: AxiosRequestConfig): AxiosInstance {
    return setupAxios(options);
  }

  public cancelToken() {
    return axios.CancelToken.source().token;
  }

  public redirectToLogin() {
    const url =
      !this.config("with_authentication") && this.config("custom_login_path")
        ? this.config("custom_login_path")
        : this.url("/login");

    this.visit({ remote: true, url });
  }

  public visit(path: string | { url: string; remote?: boolean }, options: any = {}) {
    const openInNewTab = options.openInNewTab || false;

    if (typeof path === "string") {
      this.$router.visit(this.url(path), omit(options, ["openInNewTab"]));
    } else if (path.remote) {
      if (openInNewTab) {
        window.open(path.url, "_blank");
      } else {
        window.location.href = path.url;
      }
    } else {
      this.$router.visit(path.url, omit(options, ["openInNewTab"]));
    }
  }

  public $on(...args: [any, any, any?]) {
    this.$emitter.on(...args);
  }

  public $once(...args: [any, any, any?]) {
    this.$emitter.once(...args);
  }

  public $emit(...args: [any, any[]?]) {
    this.$emitter.emit(...args);
  }

  public $off(...args: [any, any?]) {
    this.$emitter.off(...args);
  }

  public preventRouterIfDirty(resourceFormStore: any) {
    let removeStartEventListener = this.$router.on("before", (event: any) => {
      if (resourceFormStore.form.is_dirty && !confirm("Do you really want to leave? You have unsaved changes.")) {
        event.preventDefault();
      } else {
        removeStartEventListener();
      }
    });
  }

  public get_system_theme_key() {
    return !("theme" in localStorage) ? "system" : localStorage.theme;
  }

  public get_system_theme() {
    return this.get_system_theme_key() === "system"
      ? window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light"
      : localStorage.theme;
  }

  public dark_mode() {
    return this.get_system_theme() === "dark";
  }
}
