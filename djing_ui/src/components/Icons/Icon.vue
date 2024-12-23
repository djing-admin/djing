<template>
  <component
    class="inline-block"
    :is="iconName"
    role="presentation"
    :width="width"
    :height="height"
    :viewBox="viewBox"
  />
</template>

<script setup lang="ts">
import { computed } from "vue";

const { type, solid } = defineProps({
  type: {
    type: String,
    default: "delete",
  },
  solid: {
    type: Boolean,
    default: false,
  },
});

const style = computed(() => {
  return solid ? "solid" : "outline";
});

const iconName = computed(() => {
  return `heroicons-${style.value}-${type}`;
});

const viewBox = computed(() => {
  return solid ? "0 0 20 20" : "0 0 24 24";
});

const width = computed(() => {
  return solid ? 20 : 24;
});

const height = computed(() => {
  return solid ? 20 : 24;
});
</script>
