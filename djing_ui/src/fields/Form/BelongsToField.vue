<script lang="ts" setup>
import { useFetchAvailableResources } from "@/composables/useFetchAvailableResources";
import { computed, onMounted, ref } from "vue";

const { resource_name, field, form } = defineProps({
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

const { fetchAvailableResources } = useFetchAvailableResources(
  resource_name,
  field.attribute
);

onMounted(async () => {
  await initialize_component();
});

const available_resources = ref();

const initialize_component = async () => {
  try {
    const data = await fetchAvailableResources();

    const items = data.map((action: any) => {
      return {
        label: action.display,
        value: action.value,
        disabled: false,
      };
    });

    available_resources.value = items;
  } catch (error: any) {
    Djing.error(error);
  }
};

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
    required: field.required,
    name: field.attribute,
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

const handle_change = async (value: any) => {
  emit("field_changed", value);
};
</script>

<template>
  <DefaultField
    :field="field"
    :show_help_text="show_help_text"
    :mode="mode"
    :errors="form.errors"
    v-if="available_resources"
  >
    <template #field>
      <div class="space-y-1">
        <SelectControl
          v-model:selected="field.value"
          :options="available_resources"
          @handle_change="handle_change"
          v-bind="extra_attributes"
        >
          <option value="">—</option>
        </SelectControl>
      </div>
    </template>
  </DefaultField>
</template>
