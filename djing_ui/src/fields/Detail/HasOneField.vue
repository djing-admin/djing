<script lang="ts" setup>
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
  <div>
    <IndexEmptyDialog
      v-if="!field.has_one_id"
      :resource_name="field.resource_name"
      :singular_name="field.singular_label"
    />

    <div v-else>
      <ResourceDetail
        :resource_name="field.resource_name"
        :resource_id="field.has_one_id"
        :via_resource="resource_name"
        :via_resource_id="resource_id"
        :via_relationship="field.has_one_relationship"
        :via_relationship_type="field.relationship_type"
      />
    </div>
  </div>
</template>
