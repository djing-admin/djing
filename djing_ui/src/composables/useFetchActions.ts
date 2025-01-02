import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchActions = (resource_name: any, lens: string | null) => {
  const actions_endpoint = computed(() => {
    if (lens) {
      return `/djing-api/${resource_name}/lens/${lens}/actions`;
    }

    return `/djing-api/${resource_name}/actions`;
  });

  const fetchActions = async (params: any = {}) => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(actions_endpoint.value, {
          cancelToken: Djing.cancelToken(),
          params
        }),
        300
      );

      return data;
    } catch (error) {
      throw error
    }
  }

  return {
    fetchActions,
  }
}