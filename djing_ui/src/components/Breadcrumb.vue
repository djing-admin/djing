<script setup lang="ts">
import { Link } from "@inertiajs/vue3";
import { computed } from "vue";

const { breadcrumb } = defineProps({
  breadcrumbs: {
    type: Array<Object>,
    required: true,
  },
  breadcrumb: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    required: true,
  },
});

const get_path = computed(() => {
  return Djing.url(breadcrumb.path);
});
</script>

<template>
  <div class="flex items-center space-x-2">
    <Link
      @click.stop
      :href="get_path"
      v-if="breadcrumb.path != null && index < breadcrumbs.length - 1"
      class="text-primary-500"
    >
      {{ breadcrumb.name }}
    </Link>
    <span class="text-md" v-else>{{ breadcrumb.name }}</span>
    <Icon
      v-if="index < breadcrumbs.length - 1"
      type="chevron-right"
      :solid="true"
    />
  </div>
</template>
