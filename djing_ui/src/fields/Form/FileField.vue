<script lang="ts" setup>
import { File } from "@/util/file";
import { minimum } from "@/util/minimum";
import { computed, ref, onMounted } from "vue";

const { resource_name, resource_id, field, value, form } = defineProps({
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    type: [Number, String],
  },
  field: {
    required: true,
    type: Object,
  },
  show_help_text: {
    required: true,
    type: Boolean,
  },
  value: {
    required: true,
    type: [Object, String],
  },
  form: {
    required: true,
    type: Object,
  },
  mode: {
    required: true,
  },
});

const emit = defineEmits<{
  (e: "field_changed", value: any): void;
}>();

const has_error = computed(() => {
  return form.errors.hasOwnProperty(field.attribute);
});

const error_class = computed(() => {
  return has_error.value ? ["form-control-bordered-error"] : [];
});

const file_input = ref<any>(null);

const selected_file = ref<any>(null);

onMounted(() => {
  Djing.$once("resource_updated", () => {
    remove_blob_file();
  });

  if (field.value) {
    selected_file.value = field.value;
  }
});

const default_attributes = computed(() => {
  return {
    type: field.type || "file",
    name: field.attribute,
    required: field.required,
    placeholder: field.placeholder || field.attribute,
    accept: field.accepted_types,
    class: error_class.value,
    autocomplete: "off",
    autosave: "off",
  };
});

const extra_attributes = computed(() => {
  const attrs = field.extra_attributes || {};

  return {
    ...default_attributes.value,
    ...attrs,
  };
});

const handle_file_change = (event: any) => {
  const file = event.target.files[0];

  if (file) {
    const blob_file = new Blob([file], { type: file.type });

    selected_file.value = blob_file;

    file_input.value.value = "";

    emit("field_changed", new File(blob_file, file.name));
  }
};

const is_blob_type = computed(() => {
  return selected_file.value instanceof Blob;
});

const get_blob_url = computed(() => {
  return URL.createObjectURL(selected_file.value);
});

const remove_blob_file = async () => {
  file_input.value = null;
  selected_file.value = field.value;
};

const remove_field_file = async () => {
  try {
    if (!confirm("Are you sure?")) {
      return;
    }

    const delete_field_endpoint = `/djing-api/${resource_name}/${resource_id}/delete/${field.attribute}`;

    await minimum(
      Djing.request().delete(delete_field_endpoint, {
        cancelToken: Djing.cancelToken(),
        params: {},
      }),
      300
    );

    selected_file.value = null;
  } catch (error: any) {
    Djing.error("something went wrong");
  }
};

const remove_file = async () => {
  if (is_blob_type.value) {
    await remove_blob_file();
  } else {
    await remove_field_file();
  }
};
</script>

<template>
  <DefaultField
    :field="field"
    :show_help_text="show_help_text"
    :mode="mode"
    :errors="form.errors"
  >
    <template #field>
      <div class="space-y-2">
        <div v-if="selected_file">
          <div
            class="bg-gray-50 dark:bg-gray-700 relative aspect-square flex items-center justify-center rounded-lg w-36 p-2"
          >
            <Icon
              type="x-circle"
              class="absolute -right-2 -top-2 fill-black cursor-pointer"
              @click.stop="remove_file"
            />

            <div>
              <div v-if="is_blob_type">
                <img
                  v-if="selected_file"
                  :src="get_blob_url"
                  class="aspect-square object-scale-down"
                />
              </div>

              <div v-else>
                <div class="p-4 bg-white rounded-md">
                  <Icon type="document-text" class="w-12 h-12" />
                </div>
              </div>
            </div>
          </div>

          <div class="text-xs py-2">
            <span v-if="is_blob_type">
              {{ typeof value === "string" ? value : value.file_name }}
            </span>

            <span v-else>
              {{ field.value }}
            </span>
          </div>
        </div>

        <input
          v-bind="extra_attributes"
          class="w-full form-control form-input form-control-bordered"
          @input="handle_file_change"
          :name="field.attribute"
          ref="file_input"
        />
      </div>
    </template>
  </DefaultField>
</template>
