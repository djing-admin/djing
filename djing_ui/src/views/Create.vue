<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";
import { mapProps } from "@/util/propTypes";

const { resource_name, mode } = defineProps({
  mode: {
    type: String,
    default: "form",
    validator: (value: string) => ["modal", "form"].includes(value),
  },
  form_unique_id: {
    type: String,
  },
  ...mapProps(["resource_name"]),
});

const resourceFormStore = useResourceFormStore();

const handle_create_cancelled = async () => {
  window.history.back();
};

const handle_update_form_status = async (data: any) => {
  resourceFormStore.set_form_data(data.attribute, data.value);
  resourceFormStore.set_form_is_dirty(true);
};
</script>

<template>
  <CreateForm
    :mode="mode"
    :resource_name="resource_name"
    :should_override_meta="mode == 'form'"
    :form_unique_id="form_unique_id"
    @create_cancelled="handle_create_cancelled"
    @update_form_status="handle_update_form_status"
  />
</template>
