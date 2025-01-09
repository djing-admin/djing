<script lang="ts" setup>
import { useFetchRelatedResources } from "@/composables/useFetchRelatedResources";
import { onMounted } from "vue";

const { fetchRelatedResources } = useFetchRelatedResources();

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
    required: true,
    type: String,
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

onMounted(async () => {
  if (field.has_one_id) {
    await handleFetchRelatedResources();
  }
});

const handleFetchRelatedResources = async () => {
  try {
    const data = await fetchRelatedResources(field);

    console.log({ data });

    // data.panels.forEach((panel: any) => {
    //   resourceDetailStore.data.panels.push(panel);
    // });
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};
</script>

<template>
  <div>
    <IndexEmptyDialog
      v-if="!field.has_one_id"
      :resource_name="field.resource_name"
      :singular_name="field.singular_label"
    />

    <div v-else>hello</div>
  </div>
</template>
