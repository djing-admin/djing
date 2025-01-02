<script setup lang="ts">
import { mapProps } from "@/util/propTypes";
import { filter, find } from "lodash";
import { onMounted, computed, onBeforeUnmount, watch } from "vue";
import { Head } from "@inertiajs/vue3";
import { useResourceIndexStore } from "@/stores/resource_index";
import { useFetchResources } from "@/composables/useFetchResources";
import { useFetchCards } from "@/composables/useFetchCards";
import { useFetchFilters } from "@/composables/useFetchFilters";
import { useFetchActions } from "@/composables/useFetchActions";

const { resource_name, lens } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  searchable: {
    required: true,
    type: Boolean,
  },
  ...mapProps(["resource_name", "should_override_meta"]),
});

const resourceIndexStore = useResourceIndexStore();

const { fetchCards } = useFetchCards(resource_name, lens);

const { fetchFilters } = useFetchFilters(resource_name, lens);

const {
  fetchResources,
  current_filter,
  current_search,
  current_order_by,
  current_order_by_direction,
  current_page,
  current_per_page,
} = useFetchResources(resource_name, lens);

const { fetchActions } = useFetchActions(resource_name, lens);

onMounted(async () => {
  resourceIndexStore.loading = true;

  initializeSearchFromQueryString();

  initializePerPageFromQueryString();

  initializeOrderingFromQueryString();

  await handleFetchCards();

  await handleFetchFilters();

  await handleFetchResources();

  await handleFetchActions();

  watch(
    resourceIndexStore.selected_resources,
    async () => {
      await handleFetchActions();
    },
    { deep: true }
  );

  Djing.$emit("resource_loaded");
});

onBeforeUnmount(async () => {
  resourceIndexStore.reset();
});

// search
const initializeSearchFromQueryString = () => {
  resourceIndexStore.update_query("search", current_search());
};

// page
const initializePerPageFromQueryString = () => {
  resourceIndexStore.update_query(
    "per_page",
    current_per_page(resourceInformation)
  );
  resourceIndexStore.update_query("page", current_page());
};

// order
const initializeOrderingFromQueryString = () => {
  resourceIndexStore.update_query("order_by", current_order_by());

  resourceIndexStore.update_query(
    "order_by_direction",
    current_order_by_direction()
  );
};

const handleFetchCards = async () => {
  try {
    const { cards } = await fetchCards();

    resourceIndexStore.update_data("cards", cards);
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const handleFetchFilters = async () => {
  try {
    const data = await fetchFilters();

    const decoded_current_filters = JSON.parse(atob(current_filter())).map(
      (obj: any) => {
        const [key, value] = Object.entries(obj)[0];
        return {
          class: key,
          current_value: value,
        };
      }
    );

    const updated_data = data.map((filter: any) => {
      const matching_filter = decoded_current_filters.find(
        (decoded_filter: any) => decoded_filter.class === filter.class
      );

      if (matching_filter) {
        return {
          ...filter,
          current_value: matching_filter.current_value,
        };
      }

      return filter;
    });

    resourceIndexStore.update_data("filters", updated_data);

    resourceIndexStore.update_query("filter", current_filter());
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const handleFetchResources = async () => {
  try {
    const { label, pagination, resources, sortable } = await fetchResources();

    resourceIndexStore.update_data("label", label);
    resourceIndexStore.update_data("pagination", pagination);
    resourceIndexStore.update_data("resources", resources);
    resourceIndexStore.update_data("sortable", sortable);

    resourceIndexStore.loading = false;
  } catch (error: any) {
    Djing.error(error.response.data.data);
    resourceIndexStore.loading = false;
  }
};

const handleFetchActions = async () => {
  try {
    const data = await fetchActions({
      display: "index",
      resources: resourceIndexStore.get_selected_resources.length
        ? resourceIndexStore.get_selected_resources
        : null,
    });

    resourceIndexStore.update_data("actions", data.actions);
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const resourceInformation = computed(() => {
  return find(Djing.config("resources"), (resource) => {
    return resource.uri_key == resource_name;
  });
});

const resources = computed(() => {
  return resourceIndexStore.data.resources;
});

const cards = computed(() => {
  return resourceIndexStore.data.cards;
});

const should_show_card = computed(() => {
  return cards && cards.value.length > 0;
});

const should_show_pagination = computed(() => {
  return resources && resources.value.length > 0;
});

const singular_name = computed(() => {
  return resourceInformation.value.singular_label;
});

const should_show_dropdown = computed(() => {
  return standalone_actions.value.length > 0;
});

const standalone_actions = computed(() => {
  return filter(
    resourceIndexStore.data.actions,
    (action) => action.is_standalone
  );
});

const handle_action_executed = async () => {
  resourceIndexStore.reset_selected_resources();
  resourceIndexStore.reset_resources();

  await handleFetchResources();
};

const get_label = computed(() => {
  return resourceIndexStore.data.label;
});
</script>

<template>
  <LoadingView :loading="resourceIndexStore.loading">
    <Head :title="get_label" />

    <Cards
      v-if="should_show_card"
      :lens="lens"
      :cards="cards"
      :resource_name="resource_name"
    />

    <Heading
      :level="1"
      class="mb-3 flex items-center"
      :class="{
        'mt-6': should_show_card,
      }"
    >
      <span v-html="get_label" />
    </Heading>

    <div class="flex gap-2 mb-6 items-center">
      <IndexSearchInput
        v-if="resourceInformation && resourceInformation.searchable"
        :lens="lens"
        :searchable="resourceInformation && resourceInformation.searchable"
        :resource_name="resource_name"
      />

      <div class="inline-flex items-center gap-2 ml-auto">
        <ActionDropdown
          :lens="lens"
          :should_show_dropdown="should_show_dropdown"
          :resource_name="resource_name"
          :actions="standalone_actions"
          @on_action_executed="handle_action_executed"
        />
      </div>
    </div>

    <div class="relative bg-white dark:bg-gray-800 rounded-lg shadow">
      <ResourceTableToolbar
        :lens="lens"
        :resource_name="resource_name"
        :per_page_options="resourceInformation.per_page_options"
        @on_action_executed="handle_action_executed"
      />

      <LoadingView :loading="resourceIndexStore.loading">
        <IndexEmptyDialog
          v-if="!resourceIndexStore.loading && !resources.length"
          :resource_name="resource_name"
          :singular_name="singular_name"
        />

        <ResourceTable
          :lens="lens"
          :resource_name="resource_name"
          @on_action_executed="handle_action_executed"
        />

        <ResourcePagination
          v-if="should_show_pagination"
          :lens="lens"
          :resource_name="resource_name"
          :pagination="resourceIndexStore.data.pagination"
        />
      </LoadingView>
    </div>
  </LoadingView>
</template>
