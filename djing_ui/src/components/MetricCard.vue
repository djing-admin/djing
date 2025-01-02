<script lang="ts" setup>
defineProps({
  card: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div
    class="relative overflow-hidden rounded-lg shadow isolate bg-white dark:bg-gray-800 px-6 py-4 min-h-40 h-full"
  >
    <slot />
  </div>
</template>
