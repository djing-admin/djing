<script lang="ts" setup>
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

const handle_change = (value: any) => {
  emit("update:filter_changed", {
    filter_value: value,
    filter_class: props.filter.class,
  });
};
</script>

<template>
  <FilterContainer>
    <span>{{ props.filter.name }}</span>

    <template #filter>
      <input
        type="date"
        class="w-full p-2 bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md font-normal outline-none"
        :value="filter.current_value"
        @input="(event:any) => handle_change(event.target.value)"
      />
    </template>
  </FilterContainer>
</template>
