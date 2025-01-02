<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import { map } from "lodash";
import { minimum } from "@/util/minimum";
import { slug_to_title_case } from "@/util/slug_to_title_case";
import { partition_colors } from "@/util/partition_colors";

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

onMounted(async () => {
  Djing.$once("resource_loaded", async () => {
    const delay = index * 10;

    setTimeout(async () => {
      await handle_user_action();
    }, delay);
  });
});

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

const handle_user_action = async () => {
  try {
    const {
      data: { data },
    } = await minimum(
      Djing.request().get(metric_endpoint.value, {
        cancelToken: Djing.cancelToken(),
        params: {
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

const items = computed(() => {
  return map(value_result.value.value, (item: any, index: number) => {
    item["color"] = partition_colors[index];

    return item;
  });
});
</script>

<template>
  <MetricCard :card="card">
    <div v-if="value_result">
      <div class="flex justify-between">
        <div class="capitalize">{{ slug_to_title_case(card.uri_key) }}</div>

        <div>
          <span>Total: </span>
          <span v-text="value_result.total"></span>
        </div>
      </div>

      <div class="flex-row mt-4">
        <div class="flex justify-between">
          <div class="flex-1 flex-col max-h-20 overflow-auto mr-2">
            <div v-for="item in items">
              <span
                :style="{
                  background: item.color,
                  width: '10px',
                  height: '10px',
                  display: 'inline-block',
                }"
                class="mr-2 rounded-full"
              />

              <span class="mr-1">{{ item.label }}</span>

              <span>(</span>
              <span>{{ item.value }}</span>
              <span> - </span>
              <span>{{ item.percent }}%</span>
              <span>)</span>
            </div>
          </div>

          <div>
            <Doughnut :items="items" />
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <span>loading...</span>
    </div>
  </MetricCard>
</template>
