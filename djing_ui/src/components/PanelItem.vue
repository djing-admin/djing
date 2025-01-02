<script setup lang="ts">
import { computed } from "vue";

const { field, field_name } = defineProps({
  index: {
    type: Number,
    required: true,
  },
  field: {
    type: Object,
    required: true,
  },
  field_name: {
    type: String,
    required: false,
    default: null,
  },
});

const label = computed(() => {
  return field_name ?? field.name;
});
</script>

<template>
  <div class="flex p-3 -mx-6 px-6 font-normal">
    <div class="w-96">{{ label }}</div>
    <slot name="value">{{ field.displayed_as ?? field.value }}</slot>
  </div>
</template>
