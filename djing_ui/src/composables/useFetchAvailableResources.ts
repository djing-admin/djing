import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchAvailableResources = (resource_name: any, field_attribute: string) => {
  const available_resources_endpoint = computed(() => {
    return `/djing-api/${resource_name}/associatable/${field_attribute}`;
  });

  const fetchAvailableResources = async (params: any = {}) => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(available_resources_endpoint.value, {
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
    fetchAvailableResources,
  }
}