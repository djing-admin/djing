<script lang="ts" setup>
import { useDeleteResources } from "@/composables/useDeleteResources";
import { useFetchResources } from "@/composables/useFetchResources";
import { useResourceIndexStore } from "@/stores/resource_index";
import { Link } from "@inertiajs/vue3";
import { computed } from "vue";

const { lens, resource_name, resource } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource: {
    required: true,
    type: Object,
  },
});

defineEmits<{
  (e: "on_action_executed"): void;
}>();

const resourceIndexStore = useResourceIndexStore();
const { deleteResources } = useDeleteResources(resource_name);
const { fetchResources } = useFetchResources(resource_name, lens);

const resource_detail_endpoint = computed(() => {
  return Djing.url(`/resources/${resource_name}/${resource.id.value}`);
});

const resource_edit_endpoint = computed(() => {
  return Djing.url(`/resources/${resource_name}/${resource.id.value}/edit`);
});

const navigate_to_resource_detail = () => {
  if (resource.authorized_to_view && resource.id.value) {
    Djing.$router.visit(resource_detail_endpoint.value);
  }
};

const handle_delete_resource = async () => {
  try {
    await deleteResources(resource.id.value);
    await handleFetchResources();
  } catch (error: any) {
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

const authorized_to_delete = computed(() => {
  return resourceIndexStore.has_selected_resources;
});

const toggle_deletable_resource_id = () => {
  resourceIndexStore.selected_resources.all = false;

  const index = resourceIndexStore.selected_resources.ids.indexOf(
    resource.id.value
  );

  if (index === -1) {
    resourceIndexStore.selected_resources.ids.push(resource.id.value);
  } else {
    resourceIndexStore.selected_resources.ids.splice(index, 1);
  }
};

const is_checked = computed(() => {
  return resourceIndexStore.selected_resources.ids.includes(resource.id.value);
});
</script>

<template>
  <tr
    class="group"
    :class="{ 'cursor-pointer': resource.authorized_to_view }"
    @click.stop="navigate_to_resource_detail"
  >
    <td
      class="py-2 w-[1%] white-space-nowrap pl-4 pr-5 dark:bg-gray-800 group-hover:bg-gray-50 dark:group-hover:bg-gray-900"
    >
      <Checkbox
        v-if="authorized_to_delete"
        :checked="is_checked"
        @input="toggle_deletable_resource_id"
      />
    </td>

    <td
      class="px-2 py-2 whitespace-nowrap dark:bg-gray-800 group-hover:bg-gray-50 dark:group-hover:bg-gray-900"
      v-for="field in resource.fields"
    >
      <component
        :is="`index-${field.component}`"
        :field="field"
        :resource="resource"
        :resource_name="resource_name"
      />
    </td>

    <td
      class="py-2 px-2 w-[1%] white-space-nowrap text-right align-middle dark:bg-gray-800 group-hover:bg-gray-50 dark:group-hover:bg-gray-900"
    >
      <div class="flex items-center justify-end space-x-0 text-gray-400">
        <InlineActionDropdown
          :lens="lens"
          :resource="resource"
          :resource_name="resource_name"
          :resource_id="resource.id.value"
          :actions="resource.actions"
          @on_action_executed="$emit('on_action_executed')"
        />

        <div class="flex space-x-2 px-2">
          <Link
            v-if="resource.authorized_to_view"
            @click.stop
            :href="resource_detail_endpoint"
            class="hover:text-primary-500"
          >
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
                d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
              />
            </svg>
          </Link>

          <Link
            @click.stop
            :href="resource_edit_endpoint"
            class="hover:text-primary-500"
          >
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
                d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
              />
            </svg>
          </Link>

          <Button
            :disabled="!resource.authorized_to_delete"
            @click.stop="handle_delete_resource"
            :class="{
              'hover:text-primary-500': resource.authorized_to_delete,
              'text-gray-700': !resource.authorized_to_delete,
            }"
          >
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
          </Button>
        </div>
      </div>
    </td>
  </tr>
</template>
