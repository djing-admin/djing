import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useDeleteResources = (resource_name: any): any => {
  const delete_resource_url = (resources: any) => {
    return `/djing-api/${resource_name}?resources=${resources}`;
  };

  const index_resource_url = computed(() => {
    return `/resources/${resource_name}`;
  });

  const deleteResources = async (resources: any) => {
    try {
      const confirmed = confirm("Are you sure?")

      if (!confirmed) {
        return
      }

      await minimum(
        Djing.request().delete(delete_resource_url(resources), {
          cancelToken: Djing.cancelToken(),
          params: {}
        }),
        300
      );

      return { redirect_url: index_resource_url.value }
    } catch (error) {
      throw error
    }
  }

  return {
    deleteResources,
  }
}