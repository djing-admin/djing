<script lang="ts" setup>
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
    type: String,
  },
  field: {
    required: true,
    type: Object,
  },
});
</script>

<template>
  <div :class="[`text-${field.text_align}`]">
    <span v-if="field.displayed_as || field.value">
      {{
        field.displayed_as
          ? field.displayed_as.join(", ")
          : field.value.join(", ")
      }}
    </span>

    <span v-else>—</span>
  </div>
</template>
