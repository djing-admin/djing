<script lang="ts" setup>
import { ref, computed, onMounted } from "vue";
import { reduce, filter, map } from "lodash";

const { field } = defineProps({
  extra_attributes: {
    default: {
      type: "text",
      autocomplete: "off",
      autosave: "off",
    },
    type: Object,
  },
  field: {
    required: true,
    type: Object,
  },
  can_delete_row: {
    default: false,
    type: Boolean,
  },
  can_add_row: {
    default: false,
    type: Boolean,
  },
  readonly_keys: {
    default: true,
    type: Boolean,
  },
  readonly_values: {
    default: true,
    type: Boolean,
  },
});

const meta_items = ref<Array<any>>([]);

onMounted(() => {
  Djing.$on("resource_updated", () => {
    meta_items.value = [...get_items.value];
  });

  meta_items.value = [...get_items.value];
});

const default_item = { key: null, value: null };

const get_items = computed(() => {
  if (field.value && field.value instanceof Object) {
    return map(Object.entries(field.value), ([key, value]) => ({ key, value }));
  }

  return [default_item];
});

const emit = defineEmits<{
  (e: "field_changed", value: any): void;
}>();

const handle_field_change = (attribute: any, row_number: any, event: any) => {
  const item = meta_items.value.length
    ? meta_items.value[row_number]
    : default_item;

  meta_items.value[row_number] = {
    ...item,
    [attribute]: event.target.value,
  };

  emit("field_changed", transform(meta_items.value));
};

const transform = (items: any[]) => {
  return reduce(
    items,
    (acc: any, item: any) => {
      if (item["key"] !== null) {
        acc[item["key"]] = item.value;
      }
      return acc;
    },
    {}
  );
};

const remove_row = (row_number: any) => {
  const updatedItems = filter(
    meta_items.value,
    (_, index) => index !== row_number
  );

  meta_items.value = [...updatedItems];

  emit("field_changed", transform(meta_items.value));
};

const add_row = () => {
  meta_items.value = [...meta_items.value, default_item];

  emit("field_changed", transform(meta_items.value));
};
</script>

<template>
  <div class="space-y-1">
    <table class="w-full rounded text-left border-collapse">
      <thead>
        <tr>
          <th class="w-48">
            <div class="p-2 bordered-head">{{ field.key_label }}</div>
          </th>
          <th class="w-full">
            <div class="p-2 bordered-head">{{ field.value_label }}</div>
          </th>
          <th class="w-48 p-2 sr-only" />
        </tr>
      </thead>

      <tbody>
        <tr v-for="(item, index) in meta_items" :key="index">
          <td class="w-48">
            <input
              v-bind="extra_attributes"
              class="w-48 p-2"
              :class="{
                'cursor-not-allowed bordered-head': readonly_keys,
                'form-input': !readonly_keys,
              }"
              :disabled="readonly_keys"
              :value="item.key"
              @input="handle_field_change('key', index, $event)"
            />
          </td>

          <td class="w-full">
            <input
              v-bind="extra_attributes"
              class="w-full p-2"
              :class="{
                'cursor-not-allowed bordered-head': readonly_values,
                'form-input': !readonly_values,
              }"
              :disabled="readonly_values"
              :value="item.value"
              @input="handle_field_change('value', index, $event)"
            />
          </td>

          <td>
            <div
              class="p-2 text-red-400 cursor-pointer"
              v-if="can_delete_row"
              @click.stop="remove_row(index)"
            >
              <Icon type="minus-circle" />
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex justify-center pt-4" v-if="can_add_row">
      <Button @click.stop="add_row" class="text-primary-500 space-x-2">
        <Icon type="plus-circle" />
        <span>{{ field.action_text }}</span>
      </Button>
    </div>
  </div>
</template>

<style scoped>
.bordered-head {
  @apply bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700;
}
</style>
