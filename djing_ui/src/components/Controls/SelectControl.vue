<script lang="ts" setup>
import { ref } from "vue";

const { selected } = defineProps({
  selected: {
    default: "",
  },
  options: {
    required: true,
    type: Array<any>,
  },
});

const emit = defineEmits<{
  (e: "handle_change", value: any): void;
}>();

const reset_selection = () => {
  select_control.value.selectedIndex = 0;
};

defineExpose({
  reset_selection,
});

const select_control = ref();

const is_disabled = (option: any) => {
  return option.hasOwnProperty("disabled") && option.disabled;
};

const is_selected = (option: any) => {
  return selected == option.value;
};

const handle_change = async (event: any) => {
  emit("handle_change", event.target.value);
};
</script>

<template>
  <select
    class="w-full p-2 bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md font-normal outline-none"
    :value="selected"
    @change="handle_change"
    ref="select_control"
  >
    <slot />

    <option
      v-for="option in options"
      :value="option.value"
      :key="option.value"
      :selected="is_selected(option)"
      :disabled="is_disabled(option)"
    >
      {{ option.label }}
    </option>
  </select>
</template>
