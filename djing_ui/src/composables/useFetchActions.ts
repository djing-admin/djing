import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchActions = (resource_name: any) => {
  const actions_endpoint = computed(() => {
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