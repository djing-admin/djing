<script lang="ts" setup>
import { computed } from "vue";
import { useResourceIndexStore } from "@/stores/resource_index";
import { filter } from "lodash";

const resourceIndexStore = useResourceIndexStore();

defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    required: true,
    type: String,
  },
  per_page_options: {
    required: true,
    type: Array,
  },
});

defineEmits<{
  (e: "on_action_executed"): void;
}>();

const authorized_to_delete = computed(() => {
  return resourceIndexStore.has_selected_resources;
});

const should_show_actions = computed(() => {
  return (
    actions.value.length && resourceIndexStore.total_selected_resources > 0
  );
});

const actions = computed(() => {
  return filter(
    resourceIndexStore.data.actions,
    (action) => !action.is_standalone
  );
});
</script>

<template>
  <div
    class="flex flex-col md:flex-row md:items-center py-3 border-b border-gray-200 dark:border-gray-700"
  >
    <div class="flex items-center flex-1">
      <div class="ml-2">
        <SelectAllDropdown
          :resources="resourceIndexStore.data.resources"
          :total_resources="resourceIndexStore.data.pagination.total"
          v-if="
            authorized_to_delete && resourceIndexStore.data.resources.length
          "
        />
      </div>

      <div class="h-9 ml-auto flex items-center pr-2 md:pr-3">
        <ActionSelector
          v-if="should_show_actions"
          :lens="lens"
          :resource_name="resource_name"
          :actions="actions"
          @on_action_executed="$emit('on_action_executed')"
        />

        <LensMenu
          v-if="!lens && resourceIndexStore.data.lenses.length > 0"
          :resource_name="resource_name"
          :lenses="resourceIndexStore.data.lenses"
        />

        <FilterMenu
          :lens="lens"
          :resource_name="resource_name"
          :per_page_options="per_page_options"
          :filters="resourceIndexStore.data.filters"
        />

        <DeleteMenu
          :lens="lens"
          :resource_name="resource_name"
          v-if="
            authorized_to_delete &&
            resourceIndexStore.selected_resources.ids.length
          "
        />
      </div>
    </div>
  </div>
</template>
