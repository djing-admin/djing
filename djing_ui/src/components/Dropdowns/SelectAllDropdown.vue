<script lang="ts" setup>
import { useResourceIndexStore } from "@/stores/resource_index";
import { computed, ref } from "vue";

const { resources, total_resources } = defineProps({
  total_resources: {
    required: true,
    type: Number,
  },
  resources: {
    required: true,
    type: Array,
  },
});

const should_show_menu = ref(false);

const resourceIndexStore = useResourceIndexStore();

const all_selected = computed(() => {
  return resourceIndexStore.all_selected;
});

const page_selected = computed(() => {
  return resourceIndexStore.page_selected;
});

const is_selected = computed(() => {
  return (
    resourceIndexStore.all_selected ||
    resourceIndexStore.page_selected ||
    resourceIndexStore.pick_selected
  );
});

const total_selected_resources = computed(() => {
  return resourceIndexStore.total_selected_resources;
});

const resource_ids = computed(() => {
  return resources.map((resource: any) => resource.id.value);
});

const toggle_ids = (type: "page" | "all") => {
  const all_selected = resourceIndexStore.all_selected;
  const page_selected = resourceIndexStore.page_selected;

  if (type === "page") {
    resourceIndexStore.selected_resources.all = false;

    if (page_selected) {
      resourceIndexStore.selected_resources.ids = [];
    } else {
      resourceIndexStore.selected_resources.ids = resource_ids.value;
    }
  }

  if (type === "all") {
    resourceIndexStore.selected_resources.all = !all_selected;
    resourceIndexStore.selected_resources.ids = resource_ids.value;
  }

  should_show_menu.value = false;
};

const reset_selection = () => {
  resourceIndexStore.selected_resources.all = false;
  resourceIndexStore.selected_resources.ids = [];
};
</script>

<template>
  <Dropdown
    :should_show_menu="should_show_menu"
    @toggle="should_show_menu = $event"
    :classes="{ 'bg-gray-200 dark:bg-black': is_selected }"
    position="left"
  >
    <template #button>
      <div class="flex space-x-2 items-center">
        <Button
          class="w-4 h-4 border border-gray-300 dark:border-gray-600 rounded"
          :class="{
            'bg-primary-400 dark:bg-primary-500': page_selected || all_selected,
            'bg-white dark:bg-black': !(page_selected || all_selected),
          }"
        >
          <Icon
            v-if="page_selected || all_selected"
            class="w-3 h-3 -mt-[8px] text-white"
            :type="all_selected ? 'check' : 'minus'"
          />
        </Button>

        <div class="flex space-x-2 items-center" v-if="is_selected">
          <div>{{ total_selected_resources }} selected</div>

          <Icon
            class="w-4 h-4 fill-gray-400 text-gray-400 font-normal"
            type="x-circle"
            :solid="true"
            @click.stop="reset_selection"
          />
        </div>

        <Icon class="w-4 h-4" type="chevron-down" />
      </div>
    </template>

    <template #menu>
      <div class="w-60 p-3 space-y-3">
        <div
          class="flex space-x-2 items-center"
          @click.stop="toggle_ids('page')"
        >
          <Button
            class="w-4 h-4 border border-gray-300 dark:border-gray-600 rounded"
            :class="{
              'bg-primary-400 dark:bg-primary-500':
                page_selected || all_selected,
              'bg-white dark:bg-black': !(page_selected || all_selected),
            }"
          >
            <Icon
              v-if="page_selected || all_selected"
              class="w-3 h-3 -mt-[8px] text-white"
              type="check"
            />
          </Button>

          <div class="flex space-x-2 items-center">
            <div>Select this page</div>

            <Badge>{{ resources.length }}</Badge>
          </div>
        </div>

        <div
          class="flex space-x-2 items-center"
          @click.stop="toggle_ids('all')"
        >
          <Button
            class="w-4 h-4 border border-gray-300 dark:border-gray-600 rounded"
            :class="{
              'bg-primary-400 dark:bg-primary-500': all_selected,
              'bg-white dark:bg-black': !all_selected,
            }"
          >
            <Icon
              v-if="all_selected"
              class="w-3 h-3 -mt-[8px] text-white"
              type="check"
            />
          </Button>

          <div class="flex space-x-2 items-center">
            <div>Select all</div>

            <Badge>{{ total_resources }}</Badge>
          </div>
        </div>
      </div>
    </template>
  </Dropdown>
</template>
