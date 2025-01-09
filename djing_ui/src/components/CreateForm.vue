<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";
import { convert_proxy_to_value } from "@/util/convert_proxy_to_value";
import { minimum } from "@/util/minimum";
import { Head } from "@inertiajs/vue3";
import { each, find, isNil, tap } from "lodash";
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

const { resource_name, from_resource_id } = defineProps({
  mode: {
    type: String,
  },
  from_resource_id: {
    type: [Number, String],
    default: null,
  },
  resource_name: {
    type: String,
  },
  should_override_meta: {
    type: Boolean,
  },
  form_unique_id: {
    type: String,
  },
});

const resourceFormStore = useResourceFormStore();

const emit = defineEmits<{
  (e: "create_cancelled"): void;
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

const submitted_via_create_resource = ref(false);
const submitted_via_create_resource_and_add_another = ref(false);

const resourceInformation = computed(() => {
  return find(Djing.config("resources"), (resource) => {
    return resource.uri_key == resource_name;
  });
});

const singular_name = computed(() => {
  return resourceInformation.value.singular_label;
});

const resource_fields_endpoint = computed(() => {
  return `/djing-api/${resource_name}/creation-fields`;
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
          edit_mode: "create",
          inline: false,
          from_resource_id,
        },
      }),
      300
    );

    resourceFormStore.update_data("fields", data.fields);
    resourceFormStore.update_data("panels", data.panels);

    resourceFormStore.loading = false;
  } catch (error: any) {
    Djing.error(error.response.data.data);
    resourceFormStore.loading = false;
  }
};

const panels = computed(() => {
  return resourceFormStore.data.panels;
});

const get_component = (panel: any) => {
  const component = `form-${panel.component}`;

  return component;
};

const submit_via_create_resource = async () => {
  submitted_via_create_resource.value = true;
  submitted_via_create_resource_and_add_another.value = false;

  await create_resource();
};

const submit_via_create_resource_and_add_another = async () => {
  submitted_via_create_resource.value = false;
  submitted_via_create_resource_and_add_another.value = true;

  await create_resource();
};

const create_resource = async () => {
  try {
    resourceFormStore.form.loading = true;

    const {
      data: { data },
    } = await create_request();

    const resource_id = data.resource[data.id];

    Djing.success("The user was created.");

    if (submitted_via_create_resource.value) {
      resourceFormStore.reset();

      Djing.visit(`/resources/${resource_name}/${resource_id}`, {
        preserveState: true,
        preserveScroll: true,
      });
    } else {
      resourceFormStore.reset_form();
    }
  } catch (error: any) {
    resourceFormStore.form.loading = false;

    if (error.response.status == 422) {
      resourceFormStore.set_form_errors(error.response.data.errors);
    } else {
      Djing.error(error.response.data.data);
    }
  }
};

const resource_store_endpoint = computed(() => {
  return `/djing-api/${resource_name}`;
});

const create_resource_form_data = () => {
  return tap(new FormData(), (formData) => {
    each(
      Object.entries(resourceFormStore.form.data),
      ([attribute, value]: [string, any]) => {
        convert_proxy_to_value(formData, attribute, value);
      }
    );

    if (!isNil(from_resource_id)) {
      formData.append("from_resource_id", from_resource_id);
    }
  });
};

const create_request = async () => {
  const form_data = create_resource_form_data();

  return await minimum(
    Djing.request().post(resource_store_endpoint.value, form_data, {
      cancelToken: Djing.cancelToken(),
      params: {
        editing: true,
        edit_mode: "create",
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
    <Head :title="`Create ${singular_name}`" />

    <form
      class="space-y-8"
      v-if="panels"
      @submit.prevent="submit_via_create_resource"
    >
      <div class="space-y-4">
        <component
          v-for="panel in panels"
          :key="panel.id"
          :is="get_component(panel)"
          :panel="panel"
          :name="panel.name"
          :resource_name="resource_name"
          :form_unique_id="form_unique_id"
          :mode="mode"
          @field_changed="on_update_form_status"
        />
      </div>

      <div
        class="flex flex-col md:flex-row md:items-center justify-center md:justify-end space-y-2 md:space-y-0 md:space-x-3"
      >
        <Button
          @click.stop="$emit('create_cancelled')"
          class="px-4 py-2 text-black dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-black"
          >Cancel</Button
        >
        <Button
          @click.stop="submit_via_create_resource_and_add_another"
          class="px-4 py-2 rounded-md bg-primary-500 dark:bg-primary-500 text-white dark:text-black hover:bg-primary-400 dark:hover:bg-primary-400"
          >Create & Add Another</Button
        >
        <Button
          type="submit"
          class="px-4 py-2 rounded-md bg-primary-500 dark:bg-primary-500 text-white dark:text-black hover:bg-primary-400 dark:hover:bg-primary-400"
        >
          Create {{ singular_name }}
        </Button>
      </div>
    </form>
  </LoadingView>
</template>
