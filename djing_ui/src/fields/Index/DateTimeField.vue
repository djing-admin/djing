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
    type: [Number, String],
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
  <div :class="[`text-${field.text_align}`]">
    <span>
      {{ formatted_value }}
    </span>
  </div>
</template>
