<script lang="ts" setup>
const { should_show_menu, classes } = defineProps({
  classes: {
    required: false,
  },
  should_show_menu: {
    required: true,
    type: Boolean,
  },
  position: {
    type: String,
    default: "right",
  },
});

const emit = defineEmits<{
  (e: "toggle", should_show_menu: boolean): void;
}>();
</script>

<template>
  <div class="relative inline-block text-left focus:outline-1">
    <!-- User-defined Button -->
    <Button
      @click.stop="emit('toggle', !should_show_menu)"
      class="cursor-pointer flex space-x-1 hover:bg-gray-200 dark:hover:bg-black p-2 rounded-md items-center"
      :class="[
        {
          'outline outline-2 outline-gray-500': should_show_menu,
        },
        classes,
      ]"
    >
      <slot name="button"></slot>
    </Button>

    <!-- Dropdown Menu -->
    <div
      v-if="should_show_menu"
      class="absolute z-50 select-none bg-white dark:bg-gray-900 shadow-lg rounded-lg border border-gray-200 dark:border-gray-700 mt-1"
      :class="{ 'right-0': position == 'right' }"
    >
      <slot name="menu"></slot>
    </div>
  </div>

  <div
    v-if="should_show_menu"
    class="z-100 fixed inset-0 cursor-default"
    @click.stop="emit('toggle', false)"
  />
</template>
