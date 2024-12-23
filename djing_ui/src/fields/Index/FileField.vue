<script lang="ts" setup>
import { computed } from "vue";

const { field } = defineProps({
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

const image_url = computed(() => {
  return field.thumbnail_url || field.preview_url;
});
</script>

<template>
  <div
    class="items-center justify-center flex"
    :class="[`text-${field.text_align}`]"
  >
    <ImageLoader
      v-if="image_url"
      :src="image_url"
      :max_width="field.max_width || field.index_width"
      :rounded="field.rounded"
      :aspect="field.aspect"
    />

    <div v-else>
      <span> — </span>
    </div>
  </div>
</template>
