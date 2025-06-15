<script lang="ts" setup>
import { Field } from "@/interfaces/field";
import { useResourceFormStore } from "@/stores/resource_form";
import { minimum } from "@/util/minimum";
import { reject } from "lodash";
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

const fields = ref<Field[]>([]);

const resourceFormStore = useResourceFormStore();

const resource_fields_endpoint = computed(() => {
  return `/djing-api/${resource_name}/${resource_id}/update-fields`;
});

const edit_mode = computed(() => {
  return field.has_one_id === null ? "create" : "update";
});

const is_editing = computed(() => {
  return field.has_one_id !== null || field.required === true;
});

const get_fields = async () => {
  try {
    const {
      data: { data },
    } = await minimum(
      Djing.request().get(resource_fields_endpoint.value, {
        cancelToken: Djing.cancelToken(),
        params: {
          editing: true,
          edit_mode: edit_mode.value,
        },
      }),
      300
    );

    fields.value = data.fields;
  } catch (error: any) {
    Djing.error(error.response.data.data);
    resourceFormStore.loading = false;
  }
};

onMounted(async () => {
  await initialize_component();
});

const initialize_component = async () => {
  try {
    await get_fields();
  } catch (error: any) {
    Djing.error(error);
  }
};

const available_fields = computed(() => {
  return reject(fields.value, (field) => {
    return (
      (["relationship_panel"].includes(field.component) &&
        ["has_one"].includes(field.fields[0].relationship_type)) ||
      field.readonly
    );
  });
});
</script>

<template>
  <Card class="my-3 py-2 px-6 divide-y divide-gray-100 dark:divide-gray-700">
    <LoadingView :loading="resourceFormStore.loading">
      <template v-if="is_editing">
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
    </LoadingView>
  </Card>
</template>
