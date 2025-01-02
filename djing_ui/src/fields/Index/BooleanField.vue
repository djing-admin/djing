<script lang="ts" setup>
import { computed } from "vue";

const props = defineProps({
  resource: {
    required: true,
    type: Object,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    type: String,
  },
  field: {
    required: true,
    type: Object,
  },
});

const get_icon_type = computed(() => {
  return props.field.value ? "check-circle" : "x-circle";
});
</script>

<template>
  <div :class="[`text-${field.text_align}`]">
    <Icon
      :type="get_icon_type"
      :class="[
        {
          'text-red-500': field.value == false,
          'text-green-500': field.value == true,
        },
      ]"
    />
  </div>
</template>
