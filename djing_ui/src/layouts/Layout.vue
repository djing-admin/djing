<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

const loading = ref(true);

const breadcrumbs_enabled = computed(() => {
  return window.Djing.config("breadcrumbs_enabled");
});

const footer = computed(() => {
  return window.Djing.config("footer");
});

defineProps({
  breadcrumbs: Array,
});

onMounted(() => {
  loading.value = false;
});
</script>

<template>
  <LoadingView :loading="loading">
    <div
      class="text-sm font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-900"
    >
      <MainHeader />

      <div>
        <div
          class="hidden lg:block lg:absolute left-0 bottom-0 lg:top-[56px] lg:bottom-auto w-60 px-3 py-8"
        >
          <MainMenu class="pb-24" />
        </div>

        <div class="p-4 md:py-8 md:px-12 lg:ml-60 space-y-8">
          <Breadcrumbs v-if="breadcrumbs_enabled" :breadcrumbs="breadcrumbs" />

          <slot />

          <Footer :footer="footer" />
        </div>
      </div>
    </div>
  </LoadingView>
</template>
