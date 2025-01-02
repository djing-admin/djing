<script lang="ts" setup>
const { pagination } = defineProps({
  pagination: {
    required: true,
    type: Object,
  },
  current_page: {
    required: true,
    type: Number,
  },
  has_previous_page: {
    required: true,
    type: Boolean,
  },
  has_next_page: {
    required: true,
    type: Boolean,
  },
});

const emit = defineEmits<{
  (e: "navigate:to", page: any): void;
}>();
</script>

<template>
  <div class="flex-1 text-left space-x-1">
    <Button
      class="text-xs font-bold py-3 px-4 focus:outline-none rounded-bl-lg focus:ring focus:ring-inset"
      :class="{
        'text-gray-300 dark:text-gray-600': !has_previous_page,
        'text-primary-400 dark:text-primary-500': has_previous_page,
      }"
      rel="prev"
      @click.stop="emit('navigate:to', current_page - 1)"
      :disabled="!has_previous_page"
    >
      Previous
    </Button>
  </div>

  <div
    class="flex-1 text-center space-x-1"
    v-if="pagination.start_record && pagination.end_record"
  >
    <span>
      <span>{{ pagination.start_record }}</span>
      <span>-</span>
      <span>{{ pagination.end_record }}</span>
    </span>
    <span>of</span>
    <span>{{ pagination.total }}</span>
  </div>

  <div class="flex-1 text-right space-x-1">
    <Button
      class="text-xs font-bold py-3 px-4 focus:outline-none rounded-bl-lg focus:ring focus:ring-inset"
      :class="{
        'text-gray-300 dark:text-gray-600': !has_next_page,
        'text-primary-400 dark:text-primary-500': has_next_page,
      }"
      rel="next"
      @click.stop="emit('navigate:to', current_page + 1)"
      :disabled="!has_next_page"
    >
      Next
    </Button>
  </div>
</template>
