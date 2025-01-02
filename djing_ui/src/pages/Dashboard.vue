<script setup lang="ts">
import Dashboard from "@/views/Dashboard.vue";

defineProps({
  name: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <Dashboard :name="name" />
</template>
