import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchCards = (resource_name: any) => {
  const cards_endpoint = computed(() => {
    return `/djing-api/${resource_name}/cards`;
  });

  const fetchCards = async (params: any = {}) => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(cards_endpoint.value, {
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
    fetchCards,
  }
}