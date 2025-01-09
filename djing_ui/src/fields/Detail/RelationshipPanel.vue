<script lang="ts" setup>
import { computed } from "vue";

const { panel } = defineProps({
  panel: {
    required: true,
    type: Object,
  },
  resource: {
    required: true,
    type: Object,
  },
  resource_id: {
    required: true,
    type: [Number, String],
  },
  resource_name: {
    required: true,
    type: String,
  },
});

const field = computed(() => {
  return panel.fields[0];
});
</script>

<template>
  <component
    :key="`${field.attribute}:${resource_id}`"
    :index="0"
    :is="`detail-${field.component}`"
    :resource="resource"
    :resource_name="resource_name"
    :resource_id="resource_id"
    :field="field"
  />
</template>
