<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";

const { panel } = defineProps({
  panel: {
    required: true,
    type: Object,
  },
  name: {
    required: true,
    type: String,
  },
  fields: {
    type: Array,
    default: [],
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
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

const field = panel.fields[0];

const relation_id = ["has_one"].includes(field.relationship_type)
  ? field.has_one_id
  : null;

const resourceFormStore = useResourceFormStore();

defineEmits<{
  (e: "field_changed", data: any): void;
}>();
</script>

<template>
  <div v-if="field.authorized_to_create">
    <Heading :level="1" :class="panel.help_text ? 'mb-2' : 'mb-3'">
      {{ name }}
    </Heading>

    <p
      v-if="panel.help_text"
      class="text-gray-500 text-sm font-semibold italic mb-3"
      v-html="panel.help_text"
    />

    <component
      :is="`form-${field.component}`"
      :resource_name="field.resource_name"
      :resource_id="relation_id"
      :via_resource="field.from.via_resource"
      :via_resource_id="field.from.via_resource_id"
      :via_relationship="field.from.via_relationship"
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
  </div>
</template>
