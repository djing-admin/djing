<script setup lang="ts">
import { onMounted, ref } from "vue";

const loading = ref(true);

onMounted(() => {
  loading.value = false;
});
</script>

<template>
  <LoadingView :loading="loading">
    <div
      class="text-sm font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-900"
    >
      <slot />
    </div>
  </LoadingView>
</template>
