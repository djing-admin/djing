<script lang="ts" setup>
import { computed } from "vue";

const { width } = defineProps({
  width: {
    default: "120",
  },
});

const styles = computed(() => {
  return {
    width: width == "auto" ? "auto" : `${width}px`,
  };
});
</script>

<template>
  <div
    :style="styles"
    class="select-none overflow-hidden bg-white dark:bg-gray-900 shadow-lg rounded-lg border border-gray-200 dark:border-gray-700"
    :class="{ 'max-w-sm lg:max-w-lg': width === 'auto' }"
  >
    <slot />
  </div>
</template>
