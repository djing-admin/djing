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
    type: String,
  },
  field: {
    required: true,
    type: Object,
  },
});
</script>

<template>
  <div :class="[`text-${field.text_align}`]">
    <span
      class="rounded inline-flex items-center justify-center border border-60"
      style="border-radius: 4px; padding: 2px"
    >
      <span
        class="block w-4 h-4"
        style="border-radius: 2px"
        :style="{ 'background-color': field.value }"
      />
    </span>
  </div>
</template>
