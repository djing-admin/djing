<script lang="ts" setup>
import { useFetchResources } from "@/composables/useFetchResources";
import { useResourceIndexStore } from "@/stores/resource_index";
import { debounce } from "lodash";
import { computed } from "vue";

const resourceIndexStore = useResourceIndexStore();

const props = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    required: true,
    type: String,
  },
});

const { getParameter, handleUrlState, fetchResources } = useFetchResources(
  props.resource_name,
  props.lens
);

const keyword = computed({
  get: () => resourceIndexStore.query.search,
  set: (value: string) => handle_search(value),
});

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

const handle_search = debounce(async (search: string) => {
  resourceIndexStore.update_query("search", search);

  await handleUrlState(getParameter("search"), search);

  await handleFetchResources();
}, 300);
</script>

<template>
  <div class="relative w-96">
    <!-- Search Icon -->
    <Icon
      type="search"
      class="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 h-5"
    />

    <!-- Search Input -->
    <input
      type="text"
      v-model="keyword"
      placeholder="Search"
      class="w-full pl-10 py-[6px] rounded-full bg-white text-black shadow-sm shadow-gray-200 dark:bg-gray-800 dark:text-white dark:shadow-gray-700 focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500 dark:focus:border-gray-400 dark:focus:ring-gray-400"
    />
    <!-- Search Icon -->
    <Icon
      type="x-circle"
      class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 h-5 cursor-pointer"
      @click.stop="handle_search('')"
      v-if="keyword"
    />
  </div>
</template>
