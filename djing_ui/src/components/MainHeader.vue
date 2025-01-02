<script setup lang="ts">
import { Link, usePage } from "@inertiajs/vue3";
import { computed, ref } from "vue";

const should_show_menu = ref(false);

const page = usePage();

const app_name = computed(() => {
  return Djing.config("app_name");
});

const home_url = computed(() => {
  return Djing.url("/");
});

const login_url = computed(() => {
  return Djing.url("/login");
});

const license_validated = computed(() => {
  return page.props.valid_license;
});

const current_user: any = computed(() => {
  return page.props.current_user;
});

const toggleMenu = () => {
  should_show_menu.value = !should_show_menu.value;
};
</script>

<template>
  <header
    class="shadow px-6 py-3 justify-between w-full bg-white dark:bg-gray-800 flex items-center h-14 shadow-b dark:border-b dark:border-gray-700"
  >
    <div class="flex space-x-4 items-center">
      <Link
        @click.stop
        :href="home_url"
        class="flex text-[16px] text-black dark:text-white items-center space-x-2"
      >
        <Icon type="globe" class="w-5 h-5" />

        <span>{{ app_name }}</span>
      </Link>

      <div
        class="text-xs font-semibold text-red-500 uppercase cursor-pointer"
        v-if="license_validated == false"
      >
        unregistered
      </div>
    </div>

    <div class="flex space-x-4 items-center">
      <ThemeDropdown />

      <div v-if="current_user">
        <UserMenu :current_user="current_user" />

        <div
          v-if="should_show_menu"
          class="z-40 fixed inset-0"
          @click.stop="toggleMenu"
        ></div>
      </div>

      <div v-else>
        <Link
          @click.stop
          :href="login_url"
          class="text-green-500 hover:underline"
        >
          Sign In
        </Link>
      </div>
    </div>
  </header>
</template>
