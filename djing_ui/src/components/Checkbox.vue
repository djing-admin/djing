<script lang="ts" setup>
defineProps({
  disabled: {
    default: false,
    type: Boolean,
  },
  checked: {
    default: false,
    type: Boolean,
  },
});

const emit = defineEmits<{
  (e: "input", value: any): void;
}>();

const handle_change = async (e: any) => {
  emit("input", e);
};
</script>

<template>
  <div
    class="w-4 h-4 border rounded border-gray-300 dark:border-gray-600 cursor-pointer"
    :class="{
      'bg-primary-400 dark:bg-primary-500': checked,
      'bg-white dark:bg-black': !checked,
    }"
    :disabled="disabled"
    @click.stop
    @click.prevent="handle_change"
  >
    <Icon v-if="checked" class="w-3 h-3 -mt-[7px] text-white" type="check" />
  </div>
</template>
