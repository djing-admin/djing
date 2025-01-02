import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchFilters = (resource_name: any, lens: string | null) => {
  const filters_endpoint = computed(() => {
    if (lens) {
      return `/djing-api/${resource_name}/lens/${lens}/filters`;
    }

    return `/djing-api/${resource_name}/filters`;
  });

  const fetchFilters = async () => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(filters_endpoint.value, {
          cancelToken: Djing.cancelToken(),
          params: {}
        }),
        300
      );

      return data;
    } catch (error) {
      throw error
    }
  }

  return {
    fetchFilters,
  }
}