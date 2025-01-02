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

const handle_change = debounce((index: number, value: any) => {
  const values = props.filter.current_value;

  values[index] = value ? value : null;

  emit("update:filter_changed", {
    filter_value: values,
    filter_class: props.filter.class,
  });
}, 300);

const min_value = computed(() => {
  return props.filter.current_value[0];
});

const max_value = computed(() => {
  return props.filter.current_value[1];
});
</script>

<template>
  <FilterContainer>
    <template #filter>
      <div class="space-y-2">
        <div>
          <span
            class="space-x-1 uppercase text-xs font-bold text-gray-600 dark:text-gray-400"
          >
            {{ props.filter.name }} - from
          </span>

          <input
            type="date"
            class="w-full p-2 bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md font-normal outline-none"
            :min="filter.field.min"
            :max="filter.field.max"
            :step="filter.field.step"
            :value="min_value"
            @input="(event:any) => handle_change(0, event.target.value)"
          />
        </div>

        <div>
          <span
            class="space-x-1 uppercase text-xs font-bold text-gray-600 dark:text-gray-400"
          >
            {{ props.filter.name }} - to
          </span>

          <input
            type="date"
            class="w-full p-2 bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md font-normal outline-none"
            :min="filter.field.min"
            :max="filter.field.max"
            :step="filter.field.step"
            :value="max_value"
            @input="(event:any) => handle_change(1, event.target.value)"
          />
        </div>
      </div>
    </template>
  </FilterContainer>
</template>
