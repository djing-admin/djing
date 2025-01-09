<script lang="ts" setup>
import { computed } from "vue";

const { field, value, form } = defineProps({
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

const emit = defineEmits<{
  (e: "field_changed", value: any): void;
}>();

const has_error = computed(() => {
  return form.errors.hasOwnProperty(field.attribute);
});

const error_class = computed(() => {
  return has_error.value ? ["form-control-bordered-error"] : [];
});

const default_value = computed(() => {
  return value === undefined || value === null || value === "" ? {} : value;
});

const default_attributes = computed(() => {
  return {
    type: field.type || "checkbox",
    name: field.attribute,
    required: field.required,
    placeholder: field.placeholder,
    class: error_class.value,
  };
});

const extra_attributes = computed(() => {
  const attrs = field.extra_attributes || {};

  return {
    ...default_attributes.value,
    ...attrs,
  };
});

const handle_input_change = (value: any) => {
  const values: any = default_value.value;

  if (!values.hasOwnProperty(value)) {
    values[value] = true;
  } else {
    delete values[value];
  }

  emit("field_changed", Object.keys(values).length > 0 ? values : "");
};

const is_checked = (name: any) => {
  return default_value.value.hasOwnProperty(name);
};
</script>

<template>
  <DefaultField
    :field="field"
    :show_help_text="show_help_text"
    :mode="mode"
    :errors="form.errors"
  >
    <template #field>
      <ul class="space-y-1">
        <li v-for="option in field.options" class="flex space-x-2">
          <Checkbox
            v-bind="extra_attributes"
            :checked="is_checked(option.name)"
            @input="() => handle_input_change(option.name)"
          />

          <span>{{ option.label }}</span>
        </li>
      </ul>
    </template>
  </DefaultField>
</template>
