<script lang="ts" setup>
import { useDeleteResources } from "@/composables/useDeleteResources";
import { computed, ref } from "vue";

const should_show_menu = ref(false);

const { actions, resource, resource_name, resource_id } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  actions: {
    required: true,
    type: Array,
  },
  resource: {
    required: true,
    type: Object,
  },
  resource_id: {
    required: true,
    type: [Number, String],
  },
  resource_name: {
    required: true,
    type: String,
  },
});

defineEmits<{
  (e: "on_action_executed"): void;
}>();

const { deleteResources } = useDeleteResources(resource_name);

const handle_delete_resource = async () => {
  try {
    const { redirect_url } = await deleteResources(resource_id);

    Djing.visit(redirect_url);
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const handle_replicate_resource = async () => {
  Djing.visit(`/resources/${resource_name}/${resource_id}/replicate`);
};

const should_show_dropdown = computed(() => {
  return (
    actions.length > 0 ||
    resource.authorized_to_replicate ||
    resource.authorized_to_delete
  );
});
</script>

<template>
  <ActionDropdown
    :lens="lens"
    :should_show_dropdown="should_show_dropdown"
    :should_show_menu="should_show_menu"
    :resource_name="resource_name"
    :resource_id="resource_id"
    :actions="actions"
    @on_action_executed="$emit('on_action_executed')"
    @toggle="should_show_menu = $event"
  >
    <template #menu>
      <div class="p-1 w-36">
        <h6 class="p-2 text-gray-500 dark:text-white text-xs cursor-default">
          Actions
        </h6>

        <Button
          v-if="resource.authorized_to_replicate"
          class="w-full text-left text-sm rounded p-2 font-normal hover:bg-gray-100 hover:dark:bg-gray-800"
          @click.stop="handle_replicate_resource"
          >Replicate</Button
        >

        <Button
          v-if="resource.authorized_to_delete"
          class="w-full text-left text-sm rounded p-2 font-normal hover:bg-gray-100 hover:dark:bg-gray-800"
          @click.stop="handle_delete_resource"
          >Delete Resource</Button
        >
      </div>
    </template>
  </ActionDropdown>
</template>
