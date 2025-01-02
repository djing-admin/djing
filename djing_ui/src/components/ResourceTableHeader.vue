<script lang="ts" setup>
import { useFetchResources } from "@/composables/useFetchResources";
import { useResourceIndexStore } from "@/stores/resource_index";

const { lens, resource_name } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  fields: {
    required: false,
    type: Array<any>,
  },
  resource_name: {
    required: true,
    type: String,
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

const handle_order = async (order_by: string) => {
  const current_order_by = resourceIndexStore.query.order_by;
  const current_order_by_direction =
    resourceIndexStore.query.order_by_direction;

  let order_by_direction = null;

  switch (true) {
    case order_by !== current_order_by:
      order_by_direction = "asc";
      break;

    case current_order_by_direction == null:
      order_by_direction = "asc";
      break;

    case current_order_by_direction == "asc":
      order_by_direction = "desc";
      break;

    case current_order_by_direction == "desc":
      order_by_direction = null;
      break;

    default:
      order_by_direction = null;
      break;
  }

  resourceIndexStore.update_query("order_by", order_by);
  resourceIndexStore.update_query("order_by_direction", order_by_direction);

  await handleUrlState(getParameter("order_by"), order_by);
  await handleUrlState(getParameter("order_by_direction"), order_by_direction);

  await handleFetchResources();
};

const get_order_by_direction = (key: string) => {
  if (resourceIndexStore.query.order_by == key) {
    return resourceIndexStore.query.order_by_direction;
  }

  return null;
};
</script>

<template>
  <thead class="bg-gray-50 dark:bg-gray-800">
    <tr v-if="fields">
      <th
        class="w-[1%] white-space-nowrap uppercase text-xxs text-gray-500 tracking-wide pl-5 pr-2 py-2"
      >
        <span class="sr-only">Selected Resources</span>
      </th>

      <th
        :class="[`text-${field.text_align}`]"
        class="px-2 whitespace-nowrap uppercase text-gray-500 text-xxs tracking-wide py-2"
        v-for="field in fields"
      >
        <Button
          v-if="field.sortable"
          type="button"
          class="cursor-pointer inline-flex items-center focus:outline-none focus:ring ring-primary-200 dark:ring-gray-600 rounded"
          aria-sort="none"
          @click.stop="() => handle_order(field.attribute)"
        >
          <span
            class="inline-flex font-sans font-bold uppercase text-xxs tracking-wide text-gray-500"
          >
            {{ field.name }}
          </span>

          <svg
            class="ml-2 shrink-0"
            xmlns="http://www.w3.org/2000/svg"
            width="8"
            height="14"
            viewBox="0 0 8 14"
          >
            <path
              :class="{
                'fill-black dark:fill-white':
                  get_order_by_direction(field.attribute) == 'asc',
                'fill-gray-300 dark:fill-gray-500':
                  get_order_by_direction(field.attribute) != 'asc',
              }"
              d="M1.70710678 4.70710678c-.39052429.39052429-1.02368927.39052429-1.41421356 0-.3905243-.39052429-.3905243-1.02368927 0-1.41421356l3-3c.39052429-.3905243 1.02368927-.3905243 1.41421356 0l3 3c.39052429.39052429.39052429 1.02368927 0 1.41421356-.39052429.39052429-1.02368927.39052429-1.41421356 0L4 2.41421356 1.70710678 4.70710678z"
            ></path>
            <path
              :class="{
                'fill-black dark:fill-white':
                  get_order_by_direction(field.attribute) == 'desc',
                'fill-gray-300 dark:fill-gray-500':
                  get_order_by_direction(field.attribute) != 'desc',
              }"
              d="M6.29289322 9.29289322c.39052429-.39052429 1.02368927-.39052429 1.41421356 0 .39052429.39052429.39052429 1.02368928 0 1.41421358l-3 3c-.39052429.3905243-1.02368927.3905243-1.41421356 0l-3-3c-.3905243-.3905243-.3905243-1.02368929 0-1.41421358.3905243-.39052429 1.02368927-.39052429 1.41421356 0L4 11.5857864l2.29289322-2.29289318z"
            ></path>
          </svg>
        </Button>

        <span
          v-else
          class="inline-flex font-sans font-bold uppercase text-xxs tracking-wide text-gray-500"
        >
          {{ field.name }}
        </span>
      </th>

      <th class="uppercase text-xxs tracking-wide px-2 py-2">
        <span class="sr-only">Controls</span>
      </th>
    </tr>
  </thead>
</template>
