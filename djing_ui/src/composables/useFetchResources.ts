import { useResourceIndexStore } from "@/stores/resource_index";
import { minimum } from "@/util/minimum";
import { computed, reactive } from "vue";


export const useFetchResources = (resource_name: any, lens: string | null) => {
  const urlSearchParams = reactive(new URLSearchParams(window.location.search));

  const resourceIndexStore = useResourceIndexStore();

  const resources_endpoint = computed(() => {
    if (lens) {
      return `/djing-api/${resource_name}/lens/${lens}`;
    }

    return `/djing-api/${resource_name}`;
  });

  const getParameter = (name: string) => {
    if (lens) {
      return `${lens}_${name}`;
    }

    return `${resource_name}_${name}`;
  }

  const handleUrlState = async (key: string, value: any) => {
    if (value) {
      urlSearchParams.set(key, value);
    } else {
      urlSearchParams.delete(key);
    }

    const new_url = urlSearchParams.size
      ? `${window.location.pathname}?${urlSearchParams.toString()}`
      : window.location.pathname;

    window.history.replaceState(null, "", new_url);
  };

  const fetchResources = async () => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(resources_endpoint.value, {
          cancelToken: Djing.cancelToken(),
          params: resourceIndexStore.query,
        }),
        300
      );

      const resources = Djing.config('pagination') === 'load-more'
        ? [...resourceIndexStore.data.resources, ...data.resources]
        : data.resources

      return {
        label: data.label,
        pagination: {
          total: data.total,
          start_record: data.start_record,
          end_record: data.end_record,
          num_pages: data.num_pages,
          per_page: data.per_page,
        },
        resources,
        sortable: data.sortable
      }
    } catch (error) {
      throw error
    }
  }

  const getEncodedFilters = () => {
    return btoa(JSON.stringify(resourceIndexStore.available_filters)) as string
  }

  const current_filter = () => {
    const filter_parameter = getParameter("filter");

    if (urlSearchParams.has(filter_parameter)) {
      return urlSearchParams.get(filter_parameter) as string;
    } else {
      return getEncodedFilters();
    }
  };

  const current_search = () => {
    return urlSearchParams.get(getParameter("search")) || "";
  };

  const current_order_by = () => {
    return urlSearchParams.get(getParameter("order_by")) || "";
  };

  const current_order_by_direction = () => {
    return urlSearchParams.get(getParameter("order_by_direction")) || null;
  };

  const current_page = () => {
    return Number(urlSearchParams.get(getParameter("page"))) || 1;
  };

  const current_per_page = (resourceInformation: any) => {
    return (
      Number(urlSearchParams.get(getParameter("per_page"))) ||
      resourceInformation.value?.per_page_options[0] ||
      null
    );
  };

  return {
    getParameter,
    handleUrlState,
    getEncodedFilters,
    fetchResources,
    urlSearchParams,
    current_filter,
    current_search,
    current_order_by,
    current_order_by_direction,
    current_page,
    current_per_page,
  }
}