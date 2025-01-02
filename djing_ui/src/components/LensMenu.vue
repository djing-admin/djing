<script lang="ts" setup>
import { Link } from "@inertiajs/vue3";
import { ref } from "vue";

const { resource_name } = defineProps({
  resource_name: {
    required: true,
    type: String,
  },
  lenses: {
    required: true,
    type: Array<any>,
  },
});

const should_show_menu = ref(false);

const get_lens_url = (uri_key: string) => {
  return Djing.url(`/resources/${resource_name}/lens/${uri_key}`);
};
</script>

<template>
  <Dropdown
    :should_show_menu="should_show_menu"
    @toggle="should_show_menu = $event"
  >
    <template #button>
      <div class="flex items-center">
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
            d="m15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z"
          />
        </svg>

        <Icon type="chevron-down" class="w-4 h-4" />
      </div>
    </template>

    <template #menu>
      <div class="p-1 w-36">
        <Link
          :href="get_lens_url(lens.uri_key)"
          class="p-2 w-full text-left cursor-pointer inline-block hover:bg-gray-200 dark:hover:bg-gray-800"
          v-for="lens in lenses"
        >
          {{ lens.name }}
        </Link>
      </div>
    </template>
  </Dropdown>
</template>
