<script lang="ts" setup>
import { computed } from "vue";

const { field, form } = defineProps({
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

defineEmits<{
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
    type: field.type || "hidden",
    name: field.attribute,
    required: field.required,
    placeholder: field.placeholder || field.attribute,
    class: error_class.value,
    autocomplete: "off",
    autosave: "off",
    disabled: true,
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
  <div class="hidden">
    <input
      v-bind="extra_attributes"
      class="w-full form-control form-input form-control-bordered"
      :value="value"
    />
  </div>
</template>
