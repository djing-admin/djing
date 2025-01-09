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
    <a
      target="_blank"
      @click.stop
      :href="field.value"
      v-if="field.value"
      class="text-primary-500 font-semibold"
    >
      {{ field.displayed_as }}
    </a>

    <div v-else>
      <span> — </span>
    </div>
  </div>
</template>
