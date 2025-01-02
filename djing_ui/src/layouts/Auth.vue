<script setup lang="ts">
import { onMounted, ref, computed } from "vue";

const loading = ref(true);

onMounted(() => {
  loading.value = false;
});

const app_name = computed(() => {
  return Djing.config("app_name");
});
</script>

<template>
  <LoadingView :loading="loading">
    <div
      class="text-sm font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-900"
    >
      <div class="mx-auto max-w-sm flex justify-center pt-16 pb-8">
        <Heading :level="2" class="text-lg">
          {{ app_name }}
        </Heading>
      </div>

      <slot />
    </div>
  </LoadingView>
</template>
