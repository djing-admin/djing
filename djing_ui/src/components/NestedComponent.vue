<template>
  <li v-for="(item, index) in node" :key="index">
    <component :is="item.component" :item="item" />

    <ul v-if="hasChildren(item)" :class="{ hidden: should_hide_menu(item) }">
      <NestedComponent v-if="item.items" :node="item.items" :key="index" />
    </ul>
  </li>
</template>

<script setup lang="ts">
import { useDjingStore } from "@/stores/djing";

const djingStore = useDjingStore();

interface MenuItem {
  component: string;
  name: string;
  icon: string;
  collapsable: boolean;
  items?: MenuItem[];
}

defineProps({
  node: { type: Array<MenuItem>, required: true },
});

const hasChildren = (item: MenuItem): boolean => {
  return !!item.items && item.items.length > 0;
};

const should_hide_menu = (item: MenuItem) => {
  const key = `${item.component}-${item.name}`;
  return djingStore.getMainMenuState(key);
};
</script>
