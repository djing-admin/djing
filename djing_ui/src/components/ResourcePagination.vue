<script lang="ts" setup>
import { useFetchResources } from "@/composables/useFetchResources";
import { useResourceIndexStore } from "@/stores/resource_index";
import { computed } from "vue";

const { lens, resource_name, pagination } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    required: true,
    type: String,
  },
  pagination: {
    required: true,
    type: Object,
  },
});

const resourceIndexStore = useResourceIndexStore();

const { handleUrlState, getParameter, fetchResources } = useFetchResources(
  resource_name,
  lens
);

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

const navigate = async (page: number) => {
  resourceIndexStore.update_query("page", Number(page));

  if (pagination_type.value !== "load-more") {
    await handleUrlState(getParameter("page"), page);
  }

  await handleFetchResources();
};

const has_previous_page = computed(() => {
  return resourceIndexStore.query.page > 1;
});

const has_next_page = computed(() => {
  return resourceIndexStore.query.page < pagination.num_pages;
});

const pagination_type = computed(() => {
  return Djing.config("pagination");
});
</script>

<template>
  <div class="border-t border-gray-200 dark:border-gray-700">
    <div class="rounded-b-lg">
      <nav class="flex justify-between items-center">
        <component
          :is="`resource-pagination-${pagination_type}`"
          :pagination="pagination"
          :current_page="resourceIndexStore.query.page"
          :has_previous_page="has_previous_page"
          :has_next_page="has_next_page"
          @navigate:to="navigate"
        />
      </nav>
    </div>
  </div>
</template>
