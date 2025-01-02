<template>
  <div class="w-20">
    <svg
      viewBox="0 0 100 100"
      xmlns="http://www.w3.org/2000/svg"
      class="w-full h-full rounded-full"
    >
      <clipPath id="hole">
        <path
          d="M 50 0 a 50 50 0 0 1 0 100 50 50 0 0 1 0 -100 v 18 a 2 2 0 0 0 0 64 2 2 0 0 0 0 -64"
        />
      </clipPath>

      <foreignObject
        x="0"
        y="0"
        width="100"
        height="100"
        clip-path="url(#hole)"
      >
        <div
          xmlns="http://www.w3.org/1999/xhtml"
          class="w-full h-full"
          :style="{
            background: `conic-gradient(${cssString})`,
          }"
        />
      </foreignObject>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed, PropType } from "vue";

type ChartItem = {
  label: string;
  value: number;
  color: string;
};

const props = defineProps({
  items: {
    type: Array as PropType<ChartItem[]>,
    required: true,
  },
});

const totalValue = computed(() =>
  props.items.reduce((sum, item) => sum + item.value, 0)
);

const convertToPercent = (num: number) =>
  Math.round((num / totalValue.value) * 100);
const convertToDegrees = (num: number) => Math.round((num / 100) * 360);

const cssString = computed(() => {
  let cumulativeValue = 0;

  return props.items
    .map((item) => {
      const startValue = cumulativeValue;
      const endValue = cumulativeValue + item.value;
      cumulativeValue = endValue;

      const startDegrees = convertToDegrees(convertToPercent(startValue));
      const endDegrees = convertToDegrees(convertToPercent(endValue));

      return `${item.color} ${startDegrees}deg ${endDegrees}deg`;
    })
    .join(", ");
});
</script>

<style scoped>
/* Add any additional styles if needed */
</style>
