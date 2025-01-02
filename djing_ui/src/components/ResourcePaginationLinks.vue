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

const get_pagination_list = (
  start_record: number,
  end_record: number,
  current: number
): number[] => {
  const pages: number[] = [];
  const range = 2;

  current = Math.max(start_record, Math.min(current, end_record));

  let startPage = Math.max(start_record, current - range);
  let endPage = Math.min(end_record, current + range);

  if (startPage === start_record) {
    endPage = Math.min(end_record, startPage + 4);
  } else if (endPage === end_record) {
    startPage = Math.max(start_record, endPage - 4);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return pages;
};

const emit = defineEmits<{
  (e: "navigate:to", page: any): void;
}>();
</script>

<template>
  <div class="flex-1 text-left">
    <Button
      class="text-xs font-bold py-3 px-4 focus:outline-none focus:ring focus:ring-inset border-r border-gray-200 dark:border-gray-700"
      rel="next"
      @click.stop="emit('navigate:to', 1)"
      :disabled="current_page == 1"
    >
      <Icon
        type="chevron-double-left"
        class="w-3 h-3 text-gray-500 dark:text-gray-400"
      />
    </Button>

    <Button
      class="text-xs font-bold py-3 px-4 focus:outline-none focus:ring focus:ring-inset border-r border-gray-200 dark:border-gray-700"
      rel="next"
      @click.stop="emit('navigate:to', current_page - 1)"
      :disabled="!has_previous_page"
    >
      <Icon
        type="chevron-left"
        class="w-3 h-3 text-gray-500 dark:text-gray-400"
      />
    </Button>

    <Button
      class="text-xs font-bold py-3 px-4 focus:outline-none focus:ring focus:ring-inset border-r border-gray-200 dark:border-gray-700"
      :class="{
        'bg-gray-100 dark:bg-gray-700 text-black dark:text-gray-300':
          page == current_page,
      }"
      rel="prev"
      @click.stop="emit('navigate:to', page)"
      :disabled="current_page == page"
      v-for="page in get_pagination_list(1, pagination.num_pages, current_page)"
    >
      {{ page }}
    </Button>

    <Button
      class="text-xs font-bold py-3 px-4 focus:outline-none focus:ring focus:ring-inset border-r border-gray-200 dark:border-gray-700"
      rel="next"
      @click.stop="emit('navigate:to', current_page + 1)"
      :disabled="!has_next_page"
    >
      <Icon
        type="chevron-right"
        class="w-3 h-3 text-gray-500 dark:text-gray-400"
      />
    </Button>

    <Button
      class="text-xs font-bold py-3 px-4 focus:outline-none focus:ring focus:ring-inset border-r border-gray-200 dark:border-gray-700"
      rel="next"
      @click.stop="emit('navigate:to', pagination.num_pages)"
      :disabled="current_page == pagination.num_pages"
    >
      <Icon
        type="chevron-double-right"
        class="w-3 h-3 text-gray-500 dark:text-gray-400"
      />
    </Button>
  </div>

  <div
    class="flex-1 text-right space-x-1 mx-5"
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
</template>
