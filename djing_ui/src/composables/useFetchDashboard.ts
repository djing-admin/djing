import { minimum } from "@/util/minimum";
import { computed } from "vue";


export const useFetchDashboard = (dashboard_name: any) => {
  const dashboard_endpoint = computed(() => {
    return `/djing-api/dashboards/${dashboard_name}`;
  });

  const fetchDashboard = async () => {
    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(dashboard_endpoint.value, {
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
    fetchDashboard,
  }
}