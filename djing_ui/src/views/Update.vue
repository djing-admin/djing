<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";
import { mapProps } from "@/util/propTypes";

const { resource_name, resource_id } = defineProps({
  form_unique_id: {
    type: String,
  },
  ...mapProps(["resource_name", "resource_id"]),
});

const resourceFormStore = useResourceFormStore();

const handle_update_cancelled = async () => {
  window.history.back();
};

const handle_update_form_status = async (data: any) => {
  resourceFormStore.set_form_data(data.attribute, data.value);
  resourceFormStore.set_form_is_dirty(true);
};
</script>

<template>
  <UpdateForm
    mode="form"
    :resource_name="resource_name"
    :resource_id="resource_id"
    :form_unique_id="form_unique_id"
    :should_override_meta="true"
    @update_cancelled="handle_update_cancelled"
    @update_form_status="handle_update_form_status"
  />
</template>
