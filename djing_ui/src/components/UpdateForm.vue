<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";
import { convert_proxy_to_value } from "@/util/convert_proxy_to_value";
import { minimum } from "@/util/minimum";
import { Head } from "@inertiajs/vue3";
import { each, find, tap } from "lodash";
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

const { resource_name, resource_id } = defineProps({
  mode: {
    type: String,
  },
  form_unique_id: {
    type: String,
  },
  resource_name: {
    type: String,
  },
  resource_id: {
    type: String,
  },
  should_override_meta: {
    type: Boolean,
  },
});

const emit = defineEmits<{
  (e: "update_cancelled"): void;
  (e: "update_form_status", data: any): void;
}>();

onMounted(async () => {
  Djing.preventRouterIfDirty(resourceFormStore);

  resourceFormStore.loading = true;

  await get_fields();
});

onBeforeUnmount(async () => {
  resourceFormStore.reset();
});

const submitted_via_update_resource = ref(false);
const submitted_via_update_resource_and_continue_editing = ref(false);

const resourceInformation = computed(() => {
  return find(Djing.config("resources"), (resource) => {
    return resource.uri_key == resource_name;
  });
});

const singular_name = computed(() => {
  return resourceInformation.value.singular_label;
});

const title = computed(() => {
  return resourceFormStore.data.title;
});

const resource_fields_endpoint = computed(() => {
  return `/djing-api/${resource_name}/${resource_id}/update-fields`;
});

const get_fields = async () => {
  try {
    const {
      data: { data },
    } = await minimum(
      Djing.request().get(resource_fields_endpoint.value, {
        cancelToken: Djing.cancelToken(),
        params: {
          editing: true,
          edit_mode: "update",
        },
      }),
      300
    );

    resourceFormStore.update_data("title", data.title);
    resourceFormStore.update_data("fields", data.fields);
    resourceFormStore.update_data("panels", data.panels);

    resourceFormStore.loading = false;
  } catch (error: any) {
    Djing.error(error.response.data.data);
    resourceFormStore.loading = false;
  }
};

const resourceFormStore = useResourceFormStore();

const panels = computed(() => {
  return resourceFormStore.data.panels;
});

const get_component = (panel: any) => {
  const component = `form-${panel.component}`;

  return component;
};

const submit_via_update_resource = async () => {
  submitted_via_update_resource.value = true;
  submitted_via_update_resource_and_continue_editing.value = false;

  await update_resource();
};

const submit_via_update_resource_and_continue_editing = async () => {
  submitted_via_update_resource.value = false;
  submitted_via_update_resource_and_continue_editing.value = true;

  await update_resource();
};

const update_resource = async () => {
  try {
    resourceFormStore.form.loading = true;

    const {
      data: { data },
    } = await update_request();

    await get_fields();

    const resource_id = data.resource[data.id];

    Djing.success("The user was updated.");

    if (submitted_via_update_resource.value) {
      resourceFormStore.reset();

      Djing.visit(`/resources/${resource_name}/${resource_id}`, {
        preserveState: true,
        preserveScroll: true,
      });
    } else {
      resourceFormStore.reset_form();
    }

    Djing.$emit("resource_updated");
  } catch (error: any) {
    resourceFormStore.form.loading = false;

    if (error.response.status == 422) {
      resourceFormStore.set_form_errors(error.response.data.errors);
    } else {
      Djing.error(error.response.data.data);
    }
  }
};

const resource_update_endpoint = computed(() => {
  return `/djing-api/${resource_name}/${resource_id}`;
});

const create_resource_form_data = () => {
  return tap(new FormData(), (formData) => {
    each(
      Object.entries(resourceFormStore.form_data),
      ([attribute, value]: [string, any]) => {
        convert_proxy_to_value(formData, attribute, value);
      }
    );
  });
};

const update_request = async () => {
  const form_data = create_resource_form_data();

  return await minimum(
    Djing.request().put(resource_update_endpoint.value, form_data, {
      cancelToken: Djing.cancelToken(),
      params: {
        editing: true,
        edit_mode: "update",
      },
    }),
    300
  );
};

const on_update_form_status = async (data: any) => {
  emit("update_form_status", data);
};
</script>

<template>
  <LoadingView :loading="resourceFormStore.loading">
    <Head :title="`Update ${singular_name}: ${title}`" />

    <form
      class="space-y-8"
      v-if="panels"
      @submit.prevent="submit_via_update_resource"
    >
      <div class="space-y-4">
        <component
          v-for="panel in panels"
          :key="panel.id"
          :is="get_component(panel)"
          :panel="panel"
          :name="panel.name"
          :resource_name="resource_name"
          :resource_id="resource_id"
          :form_unique_id="form_unique_id"
          :mode="mode"
          @field_changed="on_update_form_status"
        />
      </div>

      <div
        class="flex flex-col md:flex-row md:items-center justify-center md:justify-end space-y-2 md:space-y-0 md:space-x-3"
      >
        <Button
          @click.stop="$emit('update_cancelled')"
          class="px-4 py-2 text-black dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-black"
          >Cancel</Button
        >
        <Button
          @click.stop="submit_via_update_resource_and_continue_editing"
          class="px-4 py-2 rounded-md bg-primary-500 dark:bg-primary-500 text-white dark:text-black hover:bg-primary-400 dark:hover:bg-primary-400"
          >Update & Continue Editing</Button
        >
        <Button
          type="submit"
          class="px-4 py-2 rounded-md bg-primary-500 dark:bg-primary-500 text-white dark:text-black hover:bg-primary-400 dark:hover:bg-primary-400"
        >
          Update {{ singular_name }}
        </Button>
      </div>
    </form>
  </LoadingView>
</template>
