<script lang="ts" setup>
import { filter, head } from "lodash";
import { computed, ref } from "vue";

const should_show_menu = ref(false);

const { resource_name, actions } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  should_show_dropdown: {
    required: true,
    type: Boolean,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    type: [Number, String],
  },
  actions: {
    required: true,
    type: Array<any>,
  },
});

const emit = defineEmits<{
  (e: "on_action_executed"): void;
}>();

const selected_action_uri_key = ref("");

const handle_user_action = async (uri_key: string) => {
  should_show_menu.value = false;
  selected_action_uri_key.value = uri_key;
};

const selected_action = computed(() => {
  return head(
    filter(actions, (action: any) => {
      return (
        selected_action_uri_key.value.length &&
        action.uri_key === selected_action_uri_key.value
      );
    })
  );
});

const handle_action_cancelled = async () => {
  if (selected_action_uri_key.value.length) {
    selected_action_uri_key.value = "";
  }
};

const handle_action_executed = async () => {
  if (selected_action_uri_key.value.length) {
    selected_action_uri_key.value = "";
  }

  emit("on_action_executed");
};
</script>

<template>
  <div>
    <component
      v-if="selected_action"
      :is="selected_action.component"
      :lens="lens"
      :resource_name="resource_name"
      :resource_id="resource_id"
      :action="selected_action"
      @on_action_cancelled="handle_action_cancelled"
      @on_action_executed="handle_action_executed"
    />

    <Dropdown
      v-if="should_show_dropdown"
      :should_show_menu="should_show_menu"
      @toggle="should_show_menu = $event"
    >
      <!-- Custom button content -->
      <template #button>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          class="size-6"
        >
          <path
            fill-rule="evenodd"
            d="M4.5 12a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0Zm6 0a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0Zm6 0a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0Z"
            clip-rule="evenodd"
          />
        </svg>
      </template>

      <template #menu>
        <slot name="menu" />

        <div class="p-1 w-48" v-if="actions.length">
          <h6 class="p-2 text-gray-500 dark:text-white text-xs cursor-default">
            User Actions
          </h6>

          <div v-for="action in actions">
            <Button
              class="w-full text-left text-sm rounded p-2 font-normal"
              :class="{
                'hover:bg-gray-100 hover:dark:bg-gray-800':
                  action.authorized_to_run != false,
                'opacity-50 cursor-default': action.authorized_to_run == false,
              }"
              @click.stop="handle_user_action(action.uri_key)"
              :disabled="action.authorized_to_run == false"
              >{{ action.name }}</Button
            >
          </div>
        </div>
      </template>
    </Dropdown>
  </div>
</template>
