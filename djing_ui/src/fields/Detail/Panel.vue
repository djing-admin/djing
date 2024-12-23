<script lang="ts" setup>
import { computed } from "vue";

const { panel } = defineProps({
  panel: {
    required: true,
    type: Object,
  },
  resource: {
    required: true,
    type: Object,
  },
  resource_id: {
    required: true,
    type: String,
  },
  resource_name: {
    required: true,
    type: String,
  },
});

const collapsed = computed(() => {
  return panel.collapsed_by_default;
});

const fields = computed(() => {
  return panel.fields;
});

const resolve_component_name = (field: any) => {
  return field.prefix_component ? "detail-" + field.component : field.component;
};
</script>

<template>
  <div>
    <slot>
      <div class="flex items-center">
        <Heading :level="1" v-text="panel.name" />
      </div>

      <p
        v-if="panel.help_text && !collapsed"
        class="text-gray-500 text-sm font-semibold italic"
        :class="panel.help_text ? 'mt-1' : 'mt-3'"
        v-html="panel.help_text"
      />
    </slot>

    <Card
      class="my-3 py-2 px-6 divide-y divide-gray-100 dark:divide-gray-700"
      v-if="!collapsed && fields.length > 0"
    >
      <component
        v-for="(field, index) in fields"
        :key="index"
        :index="index"
        :is="resolve_component_name(field)"
        :resource="resource"
        :resource_name="resource_name"
        :resource_id="resource_id"
        :field="field"
      >
        {{ resolve_component_name(field) }}
      </component>
    </Card>
  </div>
</template>
