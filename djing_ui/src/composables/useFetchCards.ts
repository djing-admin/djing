import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchCards = (resource_name: any, lens: string | null) => {
  const cards_endpoint = computed(() => {
    if (lens) {
      return `/djing-api/${resource_name}/lens/${lens}/cards`;
    }

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