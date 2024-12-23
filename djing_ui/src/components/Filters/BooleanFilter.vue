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

const is_checked = (option_name: any) => {
  return (
    props.filter.current_value.hasOwnProperty(option_name) &&
    props.filter.current_value[option_name] === true
  );
};

const handle_input_change = (option_name: any) => {
  const data = {
    ...props.filter.current_value,
    [option_name]: !is_checked(option_name),
  };

  handle_change(data);
};
</script>

<template>
  <FilterContainer>
    <span>{{ props.filter.name }}</span>

    <template #filter>
      <ul class="space-y-1">
        <li v-for="option in filter.options" class="flex space-x-2">
          <Checkbox
            :checked="is_checked(option.value)"
            @input="() => handle_input_change(option.value)"
          />

          <span>{{ option.label }}</span>
        </li>
      </ul>
    </template>
  </FilterContainer>
</template>
