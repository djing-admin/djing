<script lang="ts" setup>
import { mapProps } from "@/util/propTypes";
import ResourceCreate from "@/views/Create.vue";
import { uid } from "uid/single";
import { computed } from "vue";

const { resource_name } = defineProps(mapProps(["resource_name"]));

const form_unique_id = computed(() => {
  return uid();
});
</script>

<template>
  <ResourceCreate
    mode="form"
    :resource_name="resource_name"
    :form_unique_id="form_unique_id"
  />
</template>
