<script setup lang="ts">
import { computed, ref } from "vue";

const { field, field_name } = defineProps({
  index: {
    type: Number,
    required: true,
  },
  field: {
    type: Object,
    required: true,
  },
  field_name: {
    type: String,
    required: false,
    default: null,
  },
});

const label = computed(() => {
  return field_name ?? field.name;
});

const visible = ref(false);

const toggle_visibility = async () => {
  visible.value = !visible.value;
};
</script>

<template>
  <div class="flex p-3 -mx-6 px-6 font-normal">
    <div class="w-96">{{ label }}</div>

    <slot name="value">
      <div class="flex flex-col">
        <div v-if="visible === true">{{ field.value }}</div>

        <div
          class="space-x-1 text-primary-500 cursor-pointer font-semibold"
          :class="{ 'mt-5': visible }"
          @click.stop="toggle_visibility"
        >
          <span v-if="visible">Hide</span>
          <span v-else>Show</span>
          <span>Content</span>
        </div>
      </div>
    </slot>
  </div>
</template>
