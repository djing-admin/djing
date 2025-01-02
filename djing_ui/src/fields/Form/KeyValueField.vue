<script lang="ts" setup>
import { computed } from "vue";

const { field, form } = defineProps({
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
  show_help_text: {
    required: true,
    type: Boolean,
  },
  value: {
    required: true,
  },
  form: {
    required: true,
    type: Object,
  },
  mode: {
    required: true,
  },
});

const emit = defineEmits<{
  (e: "field_changed", value: any): void;
}>();

const default_attributes = computed(() => {
  return {
    type: field.type || "text",
    autocomplete: "off",
    autosave: "off",
  };
});

const extra_attributes = computed(() => {
  const attrs = field.extra_attributes || {};

  return {
    ...default_attributes.value,
    ...attrs,
  };
});
</script>

<template>
  <DefaultField
    :field="field"
    :show_help_text="show_help_text"
    :mode="mode"
    :errors="form.errors"
  >
    <template #field>
      <KeyValueTable
        :extra_attributes="extra_attributes"
        :field="field"
        :can_delete_row="field.can_delete_row"
        :can_add_row="field.can_add_row"
        :readonly_keys="field.readonly_keys"
        :readonly_values="false"
        @field_changed="(value:any) => emit('field_changed', value)"
      />
    </template>
  </DefaultField>
</template>
