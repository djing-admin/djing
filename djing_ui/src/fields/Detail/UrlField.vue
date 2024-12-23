<script lang="ts" setup>
defineProps({
  resource: {
    required: true,
    type: Object,
  },
  resource_name: {
    required: true,
    type: String,
  },
  resource_id: {
    required: true,
    type: String,
  },
  index: {
    required: true,
    type: Number,
  },
  field: {
    required: true,
    type: Object,
  },
});
</script>

<template>
  <PanelItem :index="index" :field="field">
    <template #value>
      <a
        target="_blank"
        @click.stop
        :href="field.value"
        v-if="field.value"
        class="text-primary-500 font-semibold"
      >
        {{ field.displayed_as }}
      </a>

      <div v-else>
        <span> — </span>
      </div>
    </template>
  </PanelItem>
</template>
