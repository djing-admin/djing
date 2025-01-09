<script lang="ts" setup>
import { formatToUTCDateTime } from "@/util/datetime";
import { computed } from "vue";

const { field } = defineProps({
  resource: {
    required: true,
    type: Object,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    required: true,
    type: [Number, String],
  },
  index: {
    required: true,
    type: Number,
  },
  field: {
    required: true,
    type: Object,
  },
});

const formatted_value = computed(() => {
  return formatToUTCDateTime(field.displayed_as ?? field.value);
});
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <span>
        {{ formatted_value }}
      </span>
    </template>
  </PanelItem>
</template>
