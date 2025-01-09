import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchResourceDetail = (resource_name: any, resource_id: any) => {
  const resource_detail_endpoint = computed(() => {
    return `/djing-api/${resource_name}/${resource_id}`;
  });

  const fetchResourceDetail = async (params: any = {}) => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(resource_detail_endpoint.value, {
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
    fetchResourceDetail,
  }
}