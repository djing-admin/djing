<script lang="ts" setup>
import { computed, onMounted, watch, ref } from "vue";
import { debounce } from "lodash";
import { title_to_slug_case } from "@/util/title_to_slug_case";

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

onMounted(() => {
  if (field.show_customize_button === true) {
    return;
  }

  watch(
    () => form.data[field.slug_from],
    debounce(async (data) => {
      emit("field_changed", title_to_slug_case(data));
    }, 300)
  );
});

const showing_customize_button = ref(field.show_customize_button);

const is_readonly = ref(extra_attributes.value.readonly);

const on_showing_customize_button = () => {
  showing_customize_button.value = false;

  is_readonly.value = false;
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
      <div class="space-y-1">
        <input
          v-if="!showing_customize_button"
          v-bind="extra_attributes"
          class="w-full form-control form-input form-control-bordered"
          :value="value"
          @input="(event:any)=> emit('field_changed', event.target.value)"
          :readonly="is_readonly"
        />

        <div v-else class="flex space-x-3">
          <input
            class="w-full form-control form-input form-control-bordered"
            disabled
            :value="value"
          />

          <Button
            v-if="field.show_customize_button"
            @click.stop="on_showing_customize_button"
            class="text-primary-500 hover:text-primary-600"
          >
            Customize
          </Button>
        </div>
      </div>
    </template>
  </DefaultField>
</template>
