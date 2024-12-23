<script setup lang="ts">
defineProps({
  breadcrumbs: Array,
});
</script>

<template>
  <div class="flex space-x-2">
    <Breadcrumb
      :breadcrumbs="breadcrumbs"
      :breadcrumb="breadcrumb"
      :index="index"
      v-for="(breadcrumb, index) in breadcrumbs"
    />
  </div>
</template>
