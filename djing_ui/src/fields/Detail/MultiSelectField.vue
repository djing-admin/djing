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
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <span v-if="field.displayed_as || field.value">
        {{
          field.displayed_as
            ? field.displayed_as.join(", ")
            : field.value.join(", ")
        }}
      </span>

      <span v-else>—</span>
    </template>
  </PanelItem>
</template>
