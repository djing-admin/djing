<script setup lang="ts">
import { mapProps } from "@/util/propTypes";

const { resource_name, lens, searchable } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  searchable: {
    required: true,
    type: Boolean,
  },
  ...mapProps(["resource_name"]),
});
</script>

<template>
  <ResourceLens
    :resource_name="resource_name"
    :lens="lens"
    :searchable="searchable"
    :should_override_meta="true"
  />
</template>
