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
    <a
      @click.stop
      :href="`mailto:${field.value}`"
      class="text-primary-500 font-semibold"
    >
      {{ field.value }}
    </a>
  </div>
</template>
