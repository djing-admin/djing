<script lang="ts" setup>
import { computed, ref } from "vue";
import { useResourceIndexStore } from "@/stores/resource_index";
import { useDeleteResources } from "@/composables/useDeleteResources";
import { useFetchResources } from "@/composables/useFetchResources";

const { lens, resource_name } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    required: true,
    type: String,
  },
});

const should_show_menu = ref(false);

const resourceIndexStore = useResourceIndexStore();
const { deleteResources } = useDeleteResources(resource_name);
const { fetchResources } = useFetchResources(resource_name, lens);

const total_selected_resources = computed(() => {
  return resourceIndexStore.total_selected_resources;
});

const selected_resources = computed(() => {
  return resourceIndexStore.get_selected_resources;
});

const handle_delete_resource = async () => {
  try {
    should_show_menu.value = false;

    await deleteResources(selected_resources.value);

    resourceIndexStore.reset_selected_resources();

    await handleFetchResources();
  } catch (error: any) {
    should_show_menu.value = false;
    Djing.error(error.response.data.data);
  }
};

const handleFetchResources = async () => {
  try {
    const { pagination, resources, sortable } = await fetchResources();

    resourceIndexStore.update_data("pagination", pagination);
    resourceIndexStore.update_data("resources", resources);
    resourceIndexStore.update_data("sortable", sortable);

    resourceIndexStore.loading = false;
  } catch (error: any) {
    Djing.error(error.response.data.data);
    resourceIndexStore.loading = false;
  }
};
</script>

<template>
  <Dropdown
    :should_show_menu="should_show_menu"
    @toggle="should_show_menu = $event"
  >
    <template #button>
      <div class="flex items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
          />
        </svg>

        <Icon type="chevron-down" class="w-4 h-4" />
      </div>
    </template>

    <template #menu>
      <div class="w-64">
        <Button
          class="py-2 px-4 space-x-2"
          @click.stop="handle_delete_resource"
        >
          <span>Delete Selected</span>
          <Badge>{{ total_selected_resources }}</Badge>
        </Button>
      </div>
    </template>
  </Dropdown>
</template>
