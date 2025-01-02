<script lang="ts" setup>
import { computed, ref } from "vue";
import { useResourceIndexStore } from "@/stores/resource_index";
import { useFetchResources } from "@/composables/useFetchResources";

const props = defineProps({
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
    type: Array<number>,
  },
  filters: {
    required: true,
    type: Array<any>,
  },
});

const should_show_menu = ref(false);

const resourceIndexStore = useResourceIndexStore();

const { getParameter, handleUrlState, getEncodedFilters, fetchResources } =
  useFetchResources(props.resource_name, props.lens);

defineEmits<{
  (
    e: "update:filter_changed",
    data: {
      filter_value: any;
      filter_class: any;
    }
  ): void;
}>();

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

const per_page_options_items = computed(() => {
  return props.per_page_options.map((per_page) => {
    return { label: per_page, value: per_page };
  });
});

const handle_per_page_changed = async (value: any) => {
  resourceIndexStore.update_query("per_page", Number(value));

  await handleUrlState(getParameter("per_page"), value);

  await handleFetchResources();
};

const handle_filter_changed = async ({
  filter_value,
  filter_class,
}: {
  filter_value: any;
  filter_class: any;
}) => {
  Object.values(resourceIndexStore.data.filters).forEach((item: any) => {
    if (item.class == filter_class) {
      item.current_value = filter_value == "—" ? "" : filter_value;
    }
  });

  const encodedFilters = getEncodedFilters();

  resourceIndexStore.update_query("filter", encodedFilters);

  await handleUrlState(getParameter("filter"), encodedFilters);

  await handleFetchResources();
};

const reset_filters = async () => {
  Object.values(resourceIndexStore.data.filters).forEach((item: any) => {
    item.current_value = item.default_value;
  });

  const encodedFilters = getEncodedFilters();

  resourceIndexStore.update_query("filter", encodedFilters);

  await handleUrlState(getParameter("filter"), encodedFilters);

  await handleFetchResources();
};
</script>

<template>
  <Dropdown
    :should_show_menu="should_show_menu"
    @toggle="should_show_menu = $event"
    :classes="{
      'bg-primary-500 dark:bg-primary-500 text-white dark:text-black hover:bg-primary-400 dark:hover:bg-primary-400':
        resourceIndexStore.applied_filters.length,
    }"
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
            d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z"
          />
        </svg>

        <div
          class="font-bold ml-1 mr-2"
          v-if="resourceIndexStore.applied_filters.length"
        >
          {{ resourceIndexStore.applied_filters.length }}
        </div>

        <Icon type="chevron-down" class="w-4 h-4" />
      </div>
    </template>

    <template #menu>
      <div class="max-h-[300px] overflow-hidden overflow-y-auto">
        <Button
          v-if="resourceIndexStore.applied_filters.length"
          class="w-full px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-center text-xs font-normal uppercase"
          @click.stop="reset_filters"
        >
          reset filters
        </Button>

        <div class="w-64">
          <div
            v-for="(filter, index) in filters"
            :key="`${filter.class}-${index}`"
          >
            <component
              :is="filter.component"
              :filter_key="filter.class"
              :filter="filter"
              :filters="filters"
              :resource_name="resource_name"
              @update:filter_changed="handle_filter_changed"
            />
          </div>

          <FilterContainer>
            <span class="block text-xs font-medium uppercase mb-1"
              >Per Page</span
            >

            <template #filter>
              <SelectControl
                v-model:selected="resourceIndexStore.query.per_page"
                :options="per_page_options_items"
                @handle_change="handle_per_page_changed"
              />
            </template>
          </FilterContainer>
        </div>
      </div>
    </template>
  </Dropdown>
</template>
