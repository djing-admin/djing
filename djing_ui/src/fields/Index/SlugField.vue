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
    type: [Number, String],
  },
  field: {
    required: true,
    type: Object,
  },
});
</script>

<template>
  <div :class="[`text-${field.text_align}`]">
    <div>
      <span> — </span>
    </div>
  </div>
</template>
