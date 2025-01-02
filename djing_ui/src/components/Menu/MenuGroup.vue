<script setup lang="ts">
import { useDjingStore } from "@/stores/djing";
import { computed, PropType } from "vue";

const djingStore = useDjingStore();

interface MenuItem {
  component: string;
  name: string;
  icon: string;
  path: string;
  collapsable: boolean;
}

const { item } = defineProps({
  item: { type: Object as PropType<MenuItem>, required: true },
});

const get_collapsable_icon_type = computed(() => {
  const menu_state = djingStore.getMainMenuState(key.value);

  return menu_state ? "chevron-right" : "chevron-down";
});

const key = computed(() => {
  return `${item.component}-${item.name}`;
});

const toggleMainMenuState = () => {
  if (item.collapsable) {
    djingStore.toggleMainMenuState(key.value);
  }
};
</script>

<template>
  <div
    class="main-menu rounded"
    :class="{
      'hover:bg-gray-200 dark:hover:bg-gray-800 cursor-pointer':
        item.collapsable,
    }"
    @click.stop="toggleMainMenuState"
  >
    <Icon :type="item.icon" class="w-6 h-6" :solid="false" v-if="item.icon" />

    <span class="w-6 h-6" v-else></span>

    <div
      class="flex-1 flex items-center w-full text-sm"
      :class="{
        uppercase: item.component == 'menu-group',
        'text-xs': item.component == 'menu-group',
      }"
    >
      {{ item.name }}
    </div>

    <Icon
      :type="get_collapsable_icon_type"
      :solid="true"
      v-if="item.collapsable"
    />
  </div>
</template>
