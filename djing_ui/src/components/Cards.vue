<script lang="ts" setup>
import { filter } from "lodash";
import { computed } from "vue";

const { cards, only_on_detail } = defineProps({
  lens: {
    default: null,
    type: String || null,
  },
  cards: {
    type: Array,
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
  only_on_detail: {
    type: Boolean,
    default: false,
  },
});

const filteredCards = computed(() => {
  if (only_on_detail) {
    return filter(cards, (card: any) => card.only_on_detail == true);
  }

  return filter(cards, (card: any) => card.only_on_detail == false);
});
</script>

<template>
  <div class="grid md:grid-cols-12 gap-6">
    <CardWrapper
      v-for="(card, index) in filteredCards"
      :lens="lens"
      :card="card"
      :index="index"
      :resource="resource"
      :resource_name="resource_name"
      :resource_id="resource_id"
      :only_on_detail="only_on_detail"
    />
  </div>
</template>
