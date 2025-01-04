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
    required: true,
    type: String,
  },
  index: {
    required: true,
    type: Number,
  },
  field: {
    required: true,
    type: Object,
  },
});

const get_url = (resource_name, resource_id) => {
  return Djing.url(`/resources/${resource_name}/${resource_id}`);
};
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <div :class="[`text-${field.text_align}`]">
        <Link
          v-if="field.value"
          @click.stop
          :href="get_url(field.resource_name, field.belongs_to_id)"
          class="text-primary-500 font-semibold"
        >
          {{ field.value }}
        </Link>

        <span v-else>{{ field.value }}</span>
      </div>
    </template>
  </PanelItem>
</template>
