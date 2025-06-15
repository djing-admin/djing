<script lang="ts" setup>
import { useFetchAvailableResources } from "@/composables/useFetchAvailableResources";
import { useResourceFormStore } from "@/stores/resource_form";
import { computed, onMounted, ref } from "vue";

const {
  resource_name,
  resource_id,
  field,
  via_resource,
  via_resource_id,
  via_relationship,
} = defineProps({
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
  show_help_text: {
    required: true,
    type: Boolean,
  },
  value: {
    required: true,
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
});

const resourceFormStore = useResourceFormStore();

const { fetchAvailableResources } = useFetchAvailableResources(
  via_resource,
  field.attribute
);

onMounted(async () => {
  await initialize_component();
});

const available_resources = ref();

const initialize_component = async () => {
  try {
    const data = await fetchAvailableResources();

    const items = data.map((action: any) => {
      return {
        label: action.display,
        value: action.value,
        disabled: action.authorized_to_add === false,
      };
    });

    available_resources.value = items;
  } catch (error: any) {
    Djing.error(error);
  }
};

const available_fields = computed(() => {
  return [];
});
</script>

<template>
  <component
    v-for="(field, index) in available_fields"
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
</template>
