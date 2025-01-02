<script lang="ts" setup>
import { computed } from "vue";

const props = defineProps({
  src: {
    type: String,
  },
  max_width: {
    type: Number,
  },
  rounded: {
    type: Boolean,
  },
  aspect: {
    type: String,
  },
});

const classes = computed(() => [props.rounded && "rounded-full"]);

const styles = computed(() => ({
  "max-width": `${props.max_width}px`,
  ...(props.aspect === "aspect-square" && { width: `${props.max_width}px` }),
  ...(props.aspect === "aspect-square" && { height: `${props.max_width}px` }),
}));
</script>

<template>
  <div>
    <img :src="src" :style="styles" :class="classes" />
  </div>
</template>
