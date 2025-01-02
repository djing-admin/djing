<script lang="ts" setup>
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

const default_value = computed(() => {
  return props.filter.current_value == null || props.filter.current_value === ""
    ? {}
    : props.filter.current_value;
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

const update_value = (option: any) => {
  const values = default_value.value;

  if (!values.hasOwnProperty(option.value)) {
    values[option.value] = true;
  } else {
    if (values[option.value] == true) {
      values[option.value] = false;
    } else {
      delete values[option.value];
    }
  }

  emit("update:filter_changed", {
    filter_value: Object.keys(values).length > 0 ? values : "",
    filter_class: props.filter.class,
  });
};

const get_icon_data = (option: any) => {
  const exists = default_value.value.hasOwnProperty(option.value);

  if (!exists) {
    return { icon: "x-circle", color: "text-gray-500" };
  } else {
    if (default_value.value[option.value] == true) {
      return { icon: "check-circle", color: "text-green-500" };
    } else {
      return { icon: "minus-circle", color: "text-red-500" };
    }
  }
};
</script>

<template>
  <FilterContainer>
    <span>{{ props.filter.name }}</span>

    <template #filter>
      <ul>
        <li
          v-for="option in props.filter.field.options"
          class="space-x-2"
          :class="get_icon_data(option).color"
        >
          <Button
            @click.stop="update_value(option)"
            class="font-normal outline-none space-x-2"
          >
            <Icon :type="get_icon_data(option).icon" />

            <span>{{ option.label }}</span>
          </Button>
        </li>
      </ul>
    </template>
  </FilterContainer>
</template>
