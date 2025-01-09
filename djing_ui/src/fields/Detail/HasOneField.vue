<script lang="ts" setup>
import { useFetchRelatedResources } from "@/composables/useFetchRelatedResources";
import { isNil } from "lodash";
import { onMounted, ref } from "vue";

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

const related_resource = ref();
const related_resource_panels = ref();
const related_resource_title = ref();

const handleFetchRelatedResources = async () => {
  try {
    const data = await fetchRelatedResources(field);

    related_resource.value = data.resource;
    related_resource_panels.value = data.panels;
    related_resource_title.value = data.title;
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const resolve_component_name = (panel: any) => {
  return isNil(panel.prefix_component) || panel.prefix_component
    ? "detail-" + panel.component
    : panel.component;
};
</script>

<template>
  <div>
    <IndexEmptyDialog
      v-if="!field.has_one_id"
      :resource_name="field.resource_name"
      :singular_name="field.singular_label"
    />

    <div v-else>
      <div v-for="panel in related_resource_panels">
        <Card class="-m-6 p-6 divide-y divide-gray-100 dark:divide-gray-700">
          <component
            v-for="(field, index) in panel.fields"
            :key="index"
            :index="index"
            :is="resolve_component_name(field)"
            :resource="resource"
            :resource_name="resource_name"
            :resource_id="resource_id"
            :field="field"
          >
            {{ resolve_component_name(field) }}
          </component>
        </Card>
      </div>
    </div>
  </div>
</template>
