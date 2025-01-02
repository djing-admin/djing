<script lang="ts" setup>
import { computed, ref } from "vue";

const { field } = defineProps({
  resource: {
    required: true,
    type: Object,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    type: String,
  },
  field: {
    required: true,
    type: Object,
  },
});

const default_value = computed(() => {
  return field.value === null || field.value === "" ? {} : field.value;
});

const has_values = computed(() => {
  return Object.keys(default_value.value).length > 0;
});

const should_show_menu = ref(false);

const get_icon_data = (option: any) => {
  const exists = default_value.value.hasOwnProperty(option.name);

  if (!exists) {
    return { icon: "x-circle", color: "text-gray-500" };
  } else {
    if (default_value.value[option.name] == true) {
      return { icon: "check-circle", color: "text-green-500" };
    } else {
      return { icon: "minus-circle", color: "text-red-500" };
    }
  }
};
</script>

<template>
  <div :class="[`text-${field.text_align}`]">
    <Dropdown
      :should_show_menu="should_show_menu"
      @toggle="should_show_menu = $event"
    >
      <!-- Custom button content -->
      <template #button>
        <span class="text-primary-500">View</span>
      </template>

      <!-- Custom dropdown menu content -->
      <template #menu>
        <div class="px-4 py-3 cursor-default">
          <ul v-if="has_values" class="space-y-2">
            <li
              v-for="option in field.options"
              class="space-x-2"
              :class="get_icon_data(option).color"
            >
              <Icon :type="get_icon_data(option).icon" />

              <span>{{ option.label }}</span>
            </li>
          </ul>

          <span v-else>{{ field.no_value_text }}</span>
        </div>
      </template>
    </Dropdown>
  </div>
</template>
