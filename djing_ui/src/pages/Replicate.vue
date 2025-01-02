<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";
import { mapProps } from "@/util/propTypes";
import { uid } from "uid/single";
import { computed } from "vue";

const { resource_name, resource_id } = defineProps({
  ...mapProps(["resource_name", "resource_id"]),
});

const resourceFormStore = useResourceFormStore();

const handle_create_cancelled = async () => {
  window.history.back();
};

const handle_update_form_status = async (data: any) => {
  resourceFormStore.set_form_data(data.attribute, data.value);
};

const form_unique_id = computed(() => {
  return uid();
});
</script>

<template>
  <CreateForm
    mode="form"
    :resource_name="resource_name"
    :from_resource_id="resource_id"
    :should_override_meta="true"
    :form_unique_id="form_unique_id"
    @create_cancelled="handle_create_cancelled"
    @update_form_status="handle_update_form_status"
  />
</template>
