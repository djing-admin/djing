import { minimum } from "@/util/minimum";

export const useFetchRelatedResources = () => {
  const build_url = (field: any) => {
    if (field.relationship_type == "has_one") {
      return `/djing-api/${field.resource_name}/${field.has_one_id}`;
    } else if (field.relationship_type == "has_many") {
      return `/djing-api/${field.resource_name}`;
    } else {
      return `/djing-api/${field.resource_name}`;
    }
  }

  const fetchRelatedResources = async (field: any, params: any = {}) => {
    const url = build_url(field)

    try {
      const {
        data: { data },
      } = await minimum(
        Djing.request().get(url, {
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
    fetchRelatedResources,
  }
}