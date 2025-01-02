<script lang="ts" setup>
import { useResourceFormStore } from "@/stores/resource_form";
import { useResourceIndexStore } from "@/stores/resource_index";
import { convert_proxy_to_value } from "@/util/convert_proxy_to_value";
import { minimum } from "@/util/minimum";
import { each, tap } from "lodash";
import { PropType, onMounted, computed } from "vue";

const { lens, action, resource_name, resource_id } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    type: String,
  },
  resource_id: {
    type: [Number, String],
  },
  form_unique_id: {
    type: String,
  },
  action: {
    type: Object as PropType<any>,
  },
});

const resourceFormStore = useResourceFormStore();
const resourceIndexStore = useResourceIndexStore();

const emit = defineEmits<{
  (e: "on_action_cancelled"): void;
  (e: "on_action_executed"): void;
}>();

onMounted(async () => {
  resourceFormStore.update_data("fields", action.fields);
});

const on_update_form_status = async (attribute: any, value: any) => {
  resourceFormStore.set_form_data(attribute, value);
  resourceFormStore.set_form_is_dirty(true);
};

const actions_endpoint = computed(() => {
  if (lens) {
    return `/djing-api/${resource_name}/lens/${lens}/actions`;
  }

  return `/djing-api/${resource_name}/actions`;
});

const get_resources = computed(() => {
  if (resource_id) {
    return resource_id;
  }

  return resourceIndexStore.get_selected_resources.length
    ? resourceIndexStore.get_selected_resources
    : null;
});

const create_resource_form_data = () => {
  return tap(new FormData(), (formData) => {
    each(
      Object.entries(resourceFormStore.form.data),
      ([attribute, value]: [string, any]) => {
        convert_proxy_to_value(formData, attribute, value);
      }
    );
  });
};

const handle_submit = async () => {
  try {
    resourceFormStore.form.loading = true;

    const form_data = create_resource_form_data();

    const {
      data: { data },
    } = await minimum(
      Djing.request().post(actions_endpoint.value, form_data, {
        cancelToken: Djing.cancelToken(),
        params: {
          action: action.uri_key,
          resources: get_resources.value,
        },
      }),
      300
    );

    resourceFormStore.reset_form();

    handle_action_response(data);

    emit("on_action_executed");
  } catch (error: any) {
    resourceFormStore.form.loading = false;

    if (error.response.status == 422) {
      resourceFormStore.set_form_errors(error.response.data.errors);
    } else {
      Djing.error(error.response.data.data);
    }
  }
};

const handle_action_response = async (data: any) => {
  if (data.response_type == "message") {
    const type = data.data.type;
    const message = data.data.message;

    if (type == "success") {
      Djing.success(message);
    } else {
      Djing.error(message);
    }
  }

  if (data.response_type == "redirect") {
    const remote = data.data.remote;
    const open_in_new_tab = data.data.open_in_new_tab;
    const url = data.data.url;
    const info = remote ? { url, remote } : url;

    Djing.visit(info, {
      openInNewTab: open_in_new_tab,
    });
  }
};
</script>

<template>
  <form class="space-y-8" @submit.prevent="handle_submit">
    <div
      class="fixed inset-0 bg-black bg-opacity-60 flex justify-center z-[1000] overflow-y-auto pointer-events-auto"
    >
      <div class="mt-5 w-[720px] relative pointer-events-auto">
        <div
          class="shadow-lg bg-gray-800 border border-gray-800 rounded-lg text-left"
        >
          <header
            class="flex justify-between items-center px-4 py-3 bg-gray-800 rounded-tr-lg rounded-tl-lg"
          >
            <h2 class="text-sm font-semibold uppercase">{{ action.name }}</h2>
          </header>

          <main class="bg-gray-800 border-t border-gray-600 space-y-2">
            <div class="pl-8 pt-6 pb-6">{{ action.confirm_text }}</div>

            <div v-if="action.fields.length">
              <component
                v-for="(field, index) in action.fields"
                :key="index"
                :index="index"
                :is="`form-${field.component}`"
                :resource_name="resource_name"
                :resource_id="resource_id"
                :form_unique_id="form_unique_id"
                :field="field"
                :mode="
                  action.modal_style === 'fullscreen'
                    ? 'action-fullscreen'
                    : 'action-modal'
                "
                :show_help_text="true"
                :value="resourceFormStore.get_field_default_value(field)"
                @field_changed="on_update_form_status(field.attribute, $event)"
              />
            </div>
          </main>

          <footer
            class="flex justify-end px-4 py-3 bg-gray-700 rounded-br-lg rounded-bl-lg space-x-2"
          >
            <Button
              @click.stop="$emit('on_action_cancelled')"
              class="px-4 py-2 text-black dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-black"
            >
              {{ action.cancel_button_text }}
            </Button>

            <Button
              type="submit"
              class="px-4 py-2 rounded-md bg-primary-500 dark:bg-primary-500 text-white dark:text-black hover:bg-primary-400 dark:hover:bg-primary-400"
            >
              {{ action.confirm_button_text }}
            </Button>
          </footer>
        </div>
      </div>
    </div>

    <div
      class="absolute z-[1000] select-none bg-red-500 dark:bg-gray-900 shadow-lg rounded-lg border border-gray-200 dark:border-gray-700 mt-1"
    />
  </form>
</template>
