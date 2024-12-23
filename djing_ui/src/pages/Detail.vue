<script lang="ts" setup>
import { mapProps } from "@/util/propTypes";

const { resource_name, resource_id } = defineProps(
  mapProps(["resource_name", "resource_id"])
);
</script>

<template>
  <ResourceDetail
    :resource_name="resource_name"
    :resource_id="resource_id"
    :should_override_meta="true"
  />
</template>
