import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchLenses = (resource_name: any) => {
  const lenses_endpoint = computed(() => {
    return `/djing-api/${resource_name}/lenses`;
  });

  const fetchLenses = async (params: any = {}) => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(lenses_endpoint.value, {
          cancelToken: Djing.cancelToken(),
          params,
        }),
        300
      );

      return data;
    } catch (error) {
      throw error
    }
  }

  return {
    fetchLenses,
  }
}