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

const update_value = () => {
  if (value.value === "") {
    value.value = true;
  } else if (value.value === true) {
    value.value = false;
  } else if (value.value === false) {
    value.value = "";
  }
};

const handle_change = (value: any) => {
  emit("update:filter_changed", {
    filter_value: value,
    filter_class: props.filter.class,
  });
};

const get_icon_type = computed(() => {
  if (value.value === true) {
    return "check-circle";
  } else if (value.value === false) {
    return "x-circle";
  } else {
    return "minus-circle";
  }
});
</script>

<template>
  <FilterContainer>
    <span>{{ props.filter.name }}</span>

    <template #filter>
      <Button @click.stop="update_value" class="font-normal outline-none">
        <Icon
          :type="get_icon_type"
          :class="[
            {
              'text-red-500': value === false,
              'text-green-500': value === true,
              'text-gray-500': value === '',
            },
          ]"
        />
      </Button>
    </template>
  </FilterContainer>
</template>
