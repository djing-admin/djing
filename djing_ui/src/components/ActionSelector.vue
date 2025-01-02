<script lang="ts" setup>
import { filter, head } from "lodash";
import { computed, ref } from "vue";

const { resource_name, actions } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  resource_name: {
    required: true,
    type: String,
  },
  actions: {
    required: true,
    type: Array<any>,
  },
});

const emit = defineEmits<{
  (e: "on_action_executed"): void;
}>();

const action_select_control = ref();

const selected_action_uri_key = ref("");

const options_for_select = computed(() => {
  return actions.map((action) => {
    return {
      label: action.name,
      value: action.uri_key,
      disabled: action.authorized_to_run === false,
    };
  });
});

const handle_user_action = async (value: any) => {
  selected_action_uri_key.value = value;
  action_select_control.value.reset_selection();
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
      :action="selected_action"
      @on_action_cancelled="handle_action_cancelled"
      @on_action_executed="handle_action_executed"
    />

    <SelectControl
      selected=""
      :options="options_for_select"
      @handle_change="handle_user_action"
      ref="action_select_control"
    >
      <option value="" disabled selected>Actions</option>
    </SelectControl>
  </div>
</template>
