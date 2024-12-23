<script lang="ts" setup>
defineProps({
  percentage: {
    type: Number,
    required: true,
  },
});
</script>

<template>
  <div
    class="w-full h-4 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-900"
  >
    <div
      class="h-full transition-all duration-300"
      :class="percentage <= 50 ? 'bg-yellow-500' : 'bg-green-500'"
      :style="{ width: `${percentage}%` }"
    >
      <slot />
    </div>
  </div>
</template>
