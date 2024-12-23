<script lang="ts" setup>
import { mapProps } from "@/util/propTypes";
import ResourceUpdate from "@/views/Update.vue";
import { uid } from "uid/single";
import { computed } from "vue";

const { resource_name, resource_id } = defineProps(
  mapProps(["resource_name", "resource_id"])
);

const form_unique_id = computed(() => {
  return uid();
});
</script>

<template>
  <ResourceUpdate
    :form_unique_id="form_unique_id"
    :resource_name="resource_name"
    :resource_id="resource_id"
  />
</template>
