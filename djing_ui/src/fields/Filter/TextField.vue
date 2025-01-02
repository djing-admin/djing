<script lang="ts" setup>
import { debounce } from "lodash";
import { computed } from "vue";

const props = defineProps({
  filter_key: {
    required: true,
    type: String,
  },
  filter: {
    required: true,
    type: Object,
  },
  filters: {
    required: true,
    type: Array<any>,
  },
  resource_name: {
    required: true,
    type: String,
  },
});

const emit = defineEmits<{
  (
    e: "update:filter_changed",
    data: {
      filter_value: any;
      filter_class: any;
    }
  ): void;
}>();

const value = computed({
  get: () => props.filter.current_value,
  set: (value: any) => handle_change(value),
});

const handle_change = debounce((value: any) => {
  emit("update:filter_changed", {
    filter_value: value,
    filter_class: props.filter.class,
  });
}, 300);
</script>

<template>
  <FilterContainer>
    <span>{{ props.filter.name }}</span>

    <template #filter>
      <input
        type="text"
        v-model="value"
        class="w-full p-2 bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md font-normal outline-none"
      />
    </template>
  </FilterContainer>
</template>
