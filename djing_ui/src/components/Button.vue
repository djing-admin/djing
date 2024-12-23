<script lang="ts" setup>
defineProps({
  variant: {
    type: String,
    default: "default",
  },
});
</script>

<template>
  <button type="button">
    <slot />
  </button>
</template>
