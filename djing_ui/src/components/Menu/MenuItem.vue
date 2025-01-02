<template>
  <Link
    @click.stop
    class="main-menu hover:bg-gray-200 dark:hover:bg-gray-800 rounded"
    :href="url"
    :class="{ 'text-primary-500': active_link, 'text-gray-500': !active_link }"
  >
    <Icon :type="item.icon" class="w-6 h-6" :solid="false" v-if="item.icon" />

    <span class="w-6 h-6" v-else></span>

    <div class="flex-1 flex items-center w-full text-sm">
      {{ item.name }}
    </div>

    <span
      v-if="item.badge"
      class="inline-flex items-center whitespace-nowrap min-h-6 px-2 rounded-full uppercase text-xs font-bold bg-sky-100 text-sky-600 dark:bg-sky-600 dark:text-sky-900"
    >
      {{ item.badge.title }}
    </span>
  </Link>
</template>

<script setup lang="ts">
import { MenuItem } from "@/interfaces/menu_item";
import { Link } from "@inertiajs/vue3";
import { computed, PropType } from "vue";

const { item } = defineProps({
  item: { type: Object as PropType<MenuItem>, required: true },
});

const url = computed(() => {
  return window.Djing.url(item.path);
});

const active_link = computed(() => {
  return item.active;
});
</script>
