<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";

defineProps({
  panel: {
    required: true,
    type: Object,
  },
  name: {
    required: true,
    type: String,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    type: [Number, String],
  },
  related_resource_name: {
    type: String,
  },
  related_resource_id: {
    type: [Number, String],
  },
  via_resource: {
    type: String,
  },
  via_resource_id: {
    type: [Number, String],
  },
  via_relationship: {
    type: String,
  },
  form_unique_id: {
    type: String,
  },
  mode: {
    required: true,
    type: String,
  },
  show_help_text: {
    default: false,
  },
  value: {
    default: "",
  },
});

const resourceFormStore = useResourceFormStore();

defineEmits<{
  (e: "field_changed", data: any): void;
}>();
</script>

<template>
  <div v-if="panel.fields.length > 0">
    <Heading :level="1" :class="panel.help_text ? 'mb-2' : 'mb-3'">
      {{ name }}
    </Heading>

    <p
      v-if="panel.help_text"
      class="text-gray-500 text-sm font-semibold italic mb-3"
      v-html="panel.help_text"
    />

    <Card class="my-3 divide-y divide-gray-100 dark:divide-gray-700">
      <component
        v-for="(field, index) in panel.fields"
        :key="index"
        :index="index"
        :is="`form-${field.component}`"
        :resource_name="resource_name"
        :resource_id="resource_id"
        :related_resource_name="resource_name"
        :related_resource_id="resource_id"
        :via_resource="via_resource"
        :via_resource_id="via_resource_id"
        :via_relationship="via_relationship"
        :form_unique_id="form_unique_id"
        :form="resourceFormStore.form"
        :field="field"
        :mode="mode"
        :show_help_text="show_help_text"
        @field_changed="
          $emit('field_changed', {
            attribute: field.attribute,
            value: $event,
          })
        "
        :value="resourceFormStore.get_field_default_value(field)"
      />
    </Card>
  </div>
</template>
