<script lang="ts" setup>
defineProps({
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
    type: [Number, String],
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
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <Icon
        :type="get_icon_type(field)"
        :class="[
          {
            'text-red-500': field.value == false,
            'text-green-500': field.value == true,
          },
        ]"
      />
    </template>
  </PanelItem>
</template>
