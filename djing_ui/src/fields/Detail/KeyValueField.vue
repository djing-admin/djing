<script lang="ts" setup>
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
    type: String,
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

const emit = defineEmits<{
  (e: "field_changed", value: any): void;
}>();

const should_display = computed(() => {
  return field.value && field.value instanceof Object;
});
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <KeyValueTable
        v-if="should_display"
        :field="field"
        :can_delete_row="false"
        :can_add_row="false"
        :readonly_keys="true"
        :readonly_values="true"
        @field_changed="(value:any) => emit('field_changed', value)"
      />

      <div v-else>
        <span> — </span>
      </div>
    </template>
  </PanelItem>
</template>
