<template>
  <component :is="component" :class="classList">
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { computed } from "vue";

const classes: Record<string, any> = {
  1: "font-normal text-xl md:text-xl",
  2: "font-normal md:text-xl",
  3: "uppercase tracking-wide font-bold text-xs",
  4: "font-normal md:text-2xl",
};

// Define props using defineProps
const props = defineProps<{
  level?: number;
}>();

// Set default values for props
const level = props.level || 1;

// Computed properties
const component = computed(() => "h" + level);
const classList = computed(() => classes[level]);
</script>
