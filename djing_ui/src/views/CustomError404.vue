<script lang="ts" setup>
import { Head, Link } from "@inertiajs/vue3";
import { computed } from "vue";

const home_url = computed(() => {
  return Djing.url("/");
});
</script>

<template>
  <Head title="Page Not Found" />

  <div class="flex items-center justify-center min-h-[500px]">
    <div>
      <img
        class="bg-transparent"
        src="https://cdn-icons-png.freepik.com/256/15614/15614740.png"
      />
    </div>

    <div class="text-left text-gray-600 dark:text-gray-400 w-96">
      <h1 class="text-[60px] font-normal mb-8">404</h1>

      <h3 class="text-[20px] font-normal mb-4">Whoops...</h3>

      <p class="text-[16px] font-normal mb-5">
        We're lost in space. The page you were trying to view does not exist.
      </p>

      <Link
        :href="home_url"
        class="block w-24 text-center text-[16px] font-normal rounded border border-gray-400 py-2 px-3"
      >
        Go Home
      </Link>
    </div>
  </div>
</template>
