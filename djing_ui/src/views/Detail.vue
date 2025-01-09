<script lang="ts" setup>
import { useFetchActions } from "@/composables/useFetchActions";
import { useFetchCards } from "@/composables/useFetchCards";
import { useFetchResourceDetail } from "@/composables/useFetchResourceDetail";
import { useResourceDetailStore } from "@/stores/resource_detail";
import { mapProps } from "@/util/propTypes";
import { Head, Link } from "@inertiajs/vue3";
import { find, isNil } from "lodash";
import { computed, onBeforeUnmount, onMounted } from "vue";

const { resource_name, resource_id } = defineProps(
  mapProps(["resource_name", "resource_id", "should_override_meta"])
);

const resourceDetailStore = useResourceDetailStore();

const { fetchCards } = useFetchCards(resource_name, null);

const { fetchResourceDetail } = useFetchResourceDetail(
  resource_name,
  resource_id
);

const { fetchActions } = useFetchActions(resource_name, null);

onMounted(async () => {
  resourceDetailStore.loading = true;

  await handleFetchCards();

  await handleFetchResourceDetail();

  await handleFetchActions();
});

onBeforeUnmount(async () => {
  resourceDetailStore.reset();
});

const resourceInformation = computed(() => {
  return find(Djing.config("resources"), (resource) => {
    return resource.uri_key == resource_name;
  });
});

const handleFetchCards = async () => {
  try {
    const { cards } = await fetchCards({ resource_id });

    resourceDetailStore.update_data("cards", cards);
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const handleFetchResourceDetail = async () => {
  try {
    const data = await fetchResourceDetail();

    resourceDetailStore.update_data("resource", data.resource);
    resourceDetailStore.update_data("panels", data.panels);
    resourceDetailStore.update_data("title", data.title);

    resourceDetailStore.loading = false;
  } catch (error: any) {
    Djing.error(error.response.data.data);
    resourceDetailStore.loading = false;
  }
};

const handleFetchActions = async () => {
  try {
    const data = await fetchActions({
      resource_id,
      editing: true,
      edit_modeL: "create",
      display: "detail",
    });

    resourceDetailStore.update_data("actions", data.actions);
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const cards = computed(() => {
  return resourceDetailStore.data.cards;
});

const should_show_card = computed(() => {
  return cards && cards.value.length > 0;
});

const resource = computed(() => {
  return resourceDetailStore.data.resource;
});

const panels = computed(() => {
  return resourceDetailStore.data.panels;
});

const title = computed(() => {
  return resourceDetailStore.data.title;
});

const resolve_component_name = (panel: any) => {
  return isNil(panel.prefix_component) || panel.prefix_component
    ? "detail-" + panel.component
    : panel.component;
};

const edit_url = (url: string) => {
  return Djing.url(url);
};

const actions = computed(() => {
  return resourceDetailStore.data.actions;
});

const handle_action_executed = async () => {
  await handleFetchResourceDetail();
};
</script>

<template>
  <LoadingView :loading="resourceDetailStore.loading">
    <Head :title="`${resourceInformation.singular_label} Detail: ${title}`" />

    <Cards
      v-if="should_show_card"
      :lens="null"
      :cards="cards"
      :resource_name="resource_name"
      :resource_id="resource_id"
      :only_on_detail="true"
    />

    <div
      :class="{
        'mt-6': should_show_card,
      }"
    >
      <div v-for="panel in panels">
        <component
          :is="resolve_component_name(panel)"
          :key="panel.id"
          :panel="panel"
          :resource="resource"
          :resource_id="resource_id"
          :resource_name="resource_name"
          class="mb-8"
        >
          <div class="md:flex items-center mb-3">
            <div class="flex flex-auto truncate items-center">
              <Heading :level="1" v-text="panel.name" />
            </div>

            <div class="ml-auto flex items-center space-x-2">
              <DetailActionDropdown
                :lens="null"
                :actions="actions"
                :resource="resource"
                :resource_id="resource_id"
                :resource_name="resource_name"
                @on_action_executed="handle_action_executed"
              />

              <Link
                @click.stop
                :href="
                  edit_url(`/resources/${resource_name}/${resource_id}/edit`)
                "
                v-if="resource.authorized_to_update"
              >
                <Button>
                  <Icon type="pencil-alt" />
                </Button>
              </Link>
            </div>
          </div>
        </component>
      </div>
    </div>
  </LoadingView>
</template>
