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
      <SelectControl
        v-model:selected="props.filter.current_value"
        :options="props.filter.options"
        @handle_change="handle_change"
      >
        <option value="">—</option>
      </SelectControl>
    </template>
  </FilterContainer>
</template>
