<script lang="ts" setup>
import { computed } from "vue";

const { field, field_name, show_help_text, errors } = defineProps({
  field: {
    required: true,
    type: Object,
  },
  field_name: {
    type: String,
  },
  show_help_text: {
    required: true,
    type: Boolean,
  },
  errors: {
    required: true,
    type: Object,
  },
  mode: {
    required: true,
  },
});

const should_show_help_text = computed(() => {
  return show_help_text && field.help_text.length > 0;
});

const label = computed(() => {
  if (field_name === "") {
    return "";
  }

  return field_name || field.name || field.singular_label;
});

const first_error = computed(() => {
  return errors.hasOwnProperty(field.attribute)
    ? errors[field.attribute][0]
    : null;
});
</script>

<template>
  <div
    v-if="field.visible"
    class="space-x-1 flex items-center py-5 px-8"
    :class="{ 'mb-2': should_show_help_text }"
  >
    <div
      v-if="field.with_label"
      class="space-x-1"
      :class="{ 'w-72': mode == 'form', 'w-36': mode != 'form' }"
    >
      <slot>
        <label class="space-x-1" :class="{ 'mb-2': should_show_help_text }">
          <span class="font-normal text-gray-500 dark:text-gray-400">
            {{ label }}
          </span>
        </label>

        <span v-if="field.required" class="text-red-500">*</span>
      </slot>
    </div>

    <div class="w-3/5">
      <slot name="field" />

      <div v-if="first_error" class="text-red-500 text-xs font-normal mt-2">
        {{ first_error }}
      </div>
    </div>
  </div>
</template>
