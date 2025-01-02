<script setup lang="ts">
import { onMounted, computed, onBeforeUnmount } from "vue";
import { Head } from "@inertiajs/vue3";
import { useDashboardStore } from "@/stores/dashboard";
import { useFetchDashboard } from "@/composables/useFetchDashboard";

const { name } = defineProps({
  name: {
    type: String,
    required: true,
  },
});

const dashboardStore = useDashboardStore();

const { fetchDashboard } = useFetchDashboard(name);

onMounted(async () => {
  dashboardStore.loading = true;

  manageFetchDashboard();
});

onBeforeUnmount(async () => {
  dashboardStore.reset();
});

const manageFetchDashboard = async () => {
  try {
    const data = await fetchDashboard();

    dashboardStore.update_data("label", data.label);
    dashboardStore.update_data("cards", data.cards);
    dashboardStore.update_data("is_help_card", data.is_help_card);
    dashboardStore.update_data("show_refresh_button", data.show_refresh_button);

    dashboardStore.loading = false;
  } catch (error: any) {
    if (error.response.status == 401) {
      return Djing.redirectToLogin();
    }

    Djing.visit("/404");
  }
};

const cards = computed(() => {
  return dashboardStore.data.cards;
});

const should_show_card = computed(() => {
  return cards && cards.value.length > 0;
});

const label = computed(() => {
  return dashboardStore.data.label;
});

const is_help_card = computed(() => {
  return dashboardStore.data.is_help_card;
});

const show_refresh_button = computed(() => {
  return dashboardStore.data.show_refresh_button;
});

const refreshDashboard = () => {
  console.log("refreshing");
};
</script>

<template>
  <LoadingView :loading="dashboardStore.loading" class="space-y-3">
    <Head :title="label" />

    <div v-if="(label && !is_help_card) || show_refresh_button">
      <Heading v-if="label && !is_help_card">
        {{ name }}
      </Heading>

      <Button @click.stop="refreshDashboard" v-if="show_refresh_button">
        <Icon type="refresh" width="14" :solid="true" />
      </Button>
    </div>

    <Cards v-if="should_show_card" :lens="null" :cards="cards" />
  </LoadingView>
</template>
