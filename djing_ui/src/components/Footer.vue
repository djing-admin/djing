<script setup lang="ts">
defineProps({
  footer: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div v-html="footer" />
</template>
