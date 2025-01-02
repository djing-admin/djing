<script lang="ts" setup>
import { Link } from "@inertiajs/vue3";

defineProps({
  resource: {
    required: true,
    type: Object,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    type: String,
  },
  field: {
    required: true,
    type: Object,
  },
});
</script>

<template>
  <div :class="[`text-${field.text_align}`]">
    <Link
      @click.stop
      :href="`/resources/${resource_name}/${field.value}`"
      v-if="resource.authorized_to_view && field.value"
      class="text-primary-500 font-semibold"
    >
      {{ field.value }}
    </Link>

    <span v-else>{{ field.value }}</span>
  </div>
</template>
