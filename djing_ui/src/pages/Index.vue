<script setup lang="ts">
import { mapProps } from "@/util/propTypes";

const { resource_name } = defineProps(mapProps(["resource_name"]));
</script>

<template>
  <ResourceIndex :resource_name="resource_name" :should_override_meta="true" />
</template>
