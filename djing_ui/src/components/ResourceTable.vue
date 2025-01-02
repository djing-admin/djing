<script lang="ts" setup>
import { useResourceIndexStore } from "@/stores/resource_index";
import { computed } from "vue";

const { resource_name } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    required: true,
    type: String,
  },
});

defineEmits<{
  (e: "on_action_executed"): void;
}>();

const resourceIndexStore = useResourceIndexStore();

const fields = computed(() => {
  return resourceIndexStore.data.resources.length
    ? resourceIndexStore.data.resources[0].fields
    : null;
});
</script>

<template>
  <table class="w-full divide-y divide-gray-100 dark:divide-gray-700">
    <ResourceTableHeader
      :lens="lens"
      :fields="fields"
      :resource_name="resource_name"
    />

    <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
      <ResourceTableRow
        v-for="resource in resourceIndexStore.data.resources"
        :lens="lens"
        :resource="resource"
        :resource_name="resource_name"
        @on_action_executed="$emit('on_action_executed')"
      />
    </tbody>
  </table>
</template>
