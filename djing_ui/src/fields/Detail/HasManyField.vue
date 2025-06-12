<script lang="ts" setup>
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
</script>

<template>
  <ResourceIndex
    :field="field"
    :resource_name="field.resource_name"
    :via_resource="resource_name"
    :via_resource_id="resource_id"
    :via_relationship="field.has_many_relationship"
    :relationship_type="field.relationship_type"
    :load_cards="false"
    :initial_per_page="field.per_page"
    :should_override_meta="false"
  />
</template>
