<template>
  <component :is="get_component" :item="item" />
</template>

<script setup lang="ts">
import { computed, PropType } from "vue";

interface MenuItem {
  component: string;
  name: string;
  icon: string;
  path: string;
  collapsable: boolean;
  active: boolean;
}

const { item } = defineProps({
  item: { type: Object as PropType<MenuItem>, required: true },
});

const get_component = computed(() => {
  return !item.collapsable && item.path ? "menu-item" : "menu-group";
});
</script>
