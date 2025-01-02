<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import { minimum } from "@/util/minimum";
import { slug_to_title_case } from "@/util/slug_to_title_case";

const { lens, card, index, resource_name, resource_id } = defineProps({
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

const options_for_select = computed(() => {
  return card.ranges;
});

onMounted(async () => {
  Djing.$once("resource_loaded", async () => {
    const delay = index * 10;

    setTimeout(async () => {
      await handle_user_action(card.ranges[0].value);
    }, delay);
  });
});

const selected_range = ref<any>(null);

const value_result = ref<any>(null);

const metric_endpoint = computed(() => {
  const lens_resource_name = lens
    ? `${resource_name}/lens/${lens}`
    : `${resource_name}`;

  if (resource_name && resource_id) {
    return `/djing-api/${lens_resource_name}/${resource_id}/metrics/${card.uri_key}`;
  }

  if (resource_name) {
    return `/djing-api/${lens_resource_name}/metrics/${card.uri_key}`;
  }

  return `/djing-api/metrics/${card.uri_key}`;
});

const handle_user_action = async (value: any) => {
  selected_range.value = value;

  try {
    const {
      data: { data },
    } = await minimum(
      Djing.request().get(metric_endpoint.value, {
        cancelToken: Djing.cancelToken(),
        params: {
          range: selected_range.value,
          timezone: "UTC",
        },
      }),
      300
    );

    value_result.value = data.value;
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const increase_or_decrease = computed(() => {
  if (
    value_result.value.previous === 0 ||
    value_result.value.previous == null ||
    value_result.value.value === 0
  ) {
    return 0;
  }

  const difference = value_result.value.value - value_result.value.previous;

  return (difference / value_result.value.value) * 100;
});

const increase_or_decrease_label = computed(() => {
  switch (Math.sign(increase_or_decrease.value)) {
    case 1:
      return "Increase";
    case 0:
      return "Constant";
    case -1:
      return "Decrease";
  }
});
</script>

<template>
  <MetricCard :card="card">
    <div v-if="value_result">
      <div class="flex justify-between">
        <div class="capitalize">{{ slug_to_title_case(card.uri_key) }}</div>

        <div>
          <SelectControl
            :selected="selected_range"
            :options="options_for_select"
            @handle_change="handle_user_action"
          />
        </div>
      </div>

      <div class="flex mt-4 space-x-4 items-center">
        <div class="p-4 bg-primary-500 rounded-lg">
          <Icon :type="card.icon" color="white" />
        </div>

        <div class="text-[40px] items-center text-center font-normal">
          <span>{{ value_result.value }}</span>

          <span class="text-xs" v-if="increase_or_decrease !== 0">
            <span>{{ increase_or_decrease }}</span>
            <span>{{ increase_or_decrease_label }}</span>
          </span>
        </div>
      </div>
    </div>

    <div v-else>
      <span>loading...</span>
    </div>
  </MetricCard>
</template>
