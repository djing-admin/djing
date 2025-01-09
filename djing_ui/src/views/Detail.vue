<script lang="ts" setup>
import { useFetchActions } from "@/composables/useFetchActions";
import { useFetchCards } from "@/composables/useFetchCards";
import { useFetchResourceDetail } from "@/composables/useFetchResourceDetail";
import { mapProps } from "@/util/propTypes";
import { Head, Link } from "@inertiajs/vue3";
import { filter, find, isNil } from "lodash";
import { computed, onBeforeUnmount, onMounted, reactive } from "vue";

const {
  via_resource,
  via_resource_id,
  via_relationship,
  via_relationship_type,
  show_view_link,
  resource_name,
  resource_id,
} = defineProps({
  via_resource: {
    type: String,
    default: null,
  },
  via_resource_id: {
    type: [String, Number],
    default: null,
  },
  via_relationship: {
    type: String,
    default: null,
  },
  via_relationship_type: {
    type: String,
    default: null,
  },
  show_view_link: {
    type: Boolean,
    default: false,
  },
  ...mapProps(["resource_name", "resource_id", "should_override_meta"]),
});

const default_store_data = {
  initial_loading: true,
  loading: true,
  data: {
    cards: [],
    panels: [],
    actions: [],
    title: null,
    resource: {},
  },
};

const resourceDetailStore = reactive(default_store_data);

const { fetchCards } = useFetchCards(resource_name, null);

const { fetchResourceDetail } = useFetchResourceDetail(
  resource_name,
  resource_id
);

const { fetchActions } = useFetchActions(resource_name, null);

onMounted(async () => {
  await initializeComponent();
});

onBeforeUnmount(async () => {
  resourceDetailStore.initial_loading = default_store_data.initial_loading;
  resourceDetailStore.loading = default_store_data.loading;
  resourceDetailStore.data = default_store_data.data;
});

const initializeComponent = async () => {
  await handleFetchCards();

  await handleFetchResourceDetail();

  await handleFetchActions();

  resourceDetailStore.initial_loading = false;
};

const resourceInformation = computed(() => {
  return find(Djing.config("resources"), (resource) => {
    return resource.uri_key == resource_name;
  });
});

const handleFetchCards = async () => {
  try {
    const { cards } = await fetchCards({ resource_id });

    resourceDetailStore.data.cards = cards;
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const handleFetchResourceDetail = async () => {
  try {
    const data = await fetchResourceDetail({
      via_resource,
      via_resource_id,
      via_relationship,
      via_relationship_type,
    });

    resourceDetailStore.data.resource = data.resource;
    resourceDetailStore.data.panels = data.panels;
    resourceDetailStore.data.title = data.title;

    handleResourceLoaded();
  } catch (error: any) {
    Djing.error(error.response.data.data);
    resourceDetailStore.loading = false;
  }
};

const handleResourceLoaded = () => {
  resourceDetailStore.loading = false;
};

const handleFetchActions = async () => {
  try {
    const data = await fetchActions({
      resource_id,
      editing: true,
      edit_modeL: "create",
      display: "detail",
    });

    resourceDetailStore.data.actions = data.actions;
  } catch (error: any) {
    Djing.error(error.response.data.data);
  }
};

const cards: any = computed(() => {
  return resourceDetailStore.data.cards;
});

const should_show_card = computed(() => {
  return cards && cards.value.length > 0;
});

const has_only_detail_cards = computed(() => {
  return filter(cards, (card) => card.only_on_detail == true);
});

const resource: any = computed(() => {
  return resourceDetailStore.data.resource;
});

const panels: any = computed(() => {
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

const get_url = (url: string) => {
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
  <LoadingView :loading="resourceDetailStore.initial_loading">
    <template v-if="should_override_meta && resourceInformation && title">
      <Head :title="`${resourceInformation.singular_label} Detail: ${title}`" />
    </template>

    <Cards
      v-if="should_show_card && has_only_detail_cards"
      :lens="null"
      :cards="cards"
      :resource_name="resource_name"
      :resource_id="resource_id"
      :only_on_detail="true"
    />

    <div
      :class="{
        'mt-6': should_show_card && has_only_detail_cards,
      }"
    >
      <component
        :is="resolve_component_name(panel)"
        v-for="panel in panels"
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
              :href="get_url(`/resources/${resource_name}/${resource_id}`)"
              v-if="show_view_link"
            >
              <Button>
                <Icon type="eye" />
              </Button>
            </Link>

            <Link
              @click.stop
              :href="get_url(`/resources/${resource_name}/${resource_id}/edit`)"
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
  </LoadingView>
</template>
