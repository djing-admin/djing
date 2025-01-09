<script lang="ts" setup>
import { computed } from "vue";

const { resource_name, resource_id, field } = defineProps({
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

const download_file = () => {
  const url = `/djing-api/${resource_name}/${resource_id}/download/${field.attribute}`;

  const link = document.createElement("a");

  link.href = url;

  link.download = url.substring(url.lastIndexOf("/") + 1);

  document.body.appendChild(link);

  link.click();

  document.body.removeChild(link);
};

const image_url = computed(() => {
  return field.thumbnail_url || field.preview_url;
});
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <div class="flex-col">
        <ImageLoader
          v-if="image_url"
          :src="image_url"
          :max_width="field.max_width || field.detail_width"
          :rounded="field.rounded"
          :aspect="field.aspect"
        />

        <div v-if="field.value && !image_url">
          <span>{{ field.value }}</span>
        </div>

        <a
          class="flex mt-3 text-gray-500 dark:text-gray-500 cursor-pointer items-center space-x-2"
          v-if="field.downloadable"
          @keydown.enter.prevent="download_file"
          @click.prevent="download_file"
        >
          <Icon type="download" class="w-4 h-4" />
          <span>Download</span>
        </a>
      </div>
    </template>
  </PanelItem>
</template>
