<script lang="ts" setup>
import { get_colspan } from "@/util/get_colspan";

defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  card: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    required: true,
  },
  resource: {
    type: Object,
    required: false,
  },
  resource_name: {
    type: String,
    default: "",
  },
  resource_id: {
    type: [Number, String],
    default: "",
  },
});
</script>

<template>
  <div :class="get_colspan(card.width)">
    <component
      :is="card.component"
      :lens="lens"
      :card="card"
      :index="index"
      :resource="resource"
      :resource_name="resource_name"
      :resource_id="resource_id"
    />
  </div>
</template>
