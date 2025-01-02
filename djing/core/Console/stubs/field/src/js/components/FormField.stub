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

const has_error = computed(() => {
  return form.errors.hasOwnProperty(field.attribute);
});

const error_class = computed(() => {
  return has_error.value ? ["form-control-bordered-error"] : [];
});

const default_attributes = computed(() => {
  return {
    type: field.type || "text",
    name: field.attribute,
    required: field.required,
    placeholder: field.placeholder || field.attribute,
    class: error_class.value,
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
      <div class="space-y-1">
        <input
          v-bind="extra_attributes"
          class="w-full form-control form-input form-control-bordered"
          :value="value"
          @input="(event:any)=> emit('field_changed', event.target.value)"
        />
      </div>
    </template>
  </DefaultField>
</template>
