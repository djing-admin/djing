<script lang="ts" setup>
import { map } from "lodash";
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

const get_icon_type = (option: any) => {
  return option.value ? "check-circle" : "x-circle";
};

const default_value = computed(() => {
  return field.value === null || field.value === "" ? {} : field.value;
});

const mapped_value = computed(() => {
  return map(field.options, (option) => {
    return {
      label: option.label,
      value: default_value.value.hasOwnProperty(option.name)
        ? default_value.value[option.name]
        : false,
    };
  });
});
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <ul v-if="mapped_value.length" class="space-y-2">
        <li
          v-for="option in mapped_value"
          class="space-x-2"
          :class="[
            {
              'text-red-500': option.value == false,
              'text-green-500': option.value == true,
            },
          ]"
        >
          <Icon :type="get_icon_type(option)" />

          <span>{{ option.label }}</span>
        </li>
      </ul>

      <span v-else>{{ field.no_value_text }}</span>
    </template>
  </PanelItem>
</template>
