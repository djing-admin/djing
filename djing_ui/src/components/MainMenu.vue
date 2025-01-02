<script setup lang="ts">
import { computed } from "vue";

import { useDjingStore } from "@/stores/djing";

const djingStore = useDjingStore();

const main_menu = computed(() => djingStore.main_menu);
</script>

<template>
  <ul class="space-y-6" v-if="main_menu.length">
    <NestedComponent :node="main_menu" />
  </ul>
</template>
