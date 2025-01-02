import { isObject } from "lodash";
import { File } from "@/util/file";

export const convert_proxy_to_value = (formData: any, attribute: any, value: any) => {
  if (isObject(value)) {
    if (value instanceof File) {
      formData.append(attribute, value.original_file, value.file_name);
    } else {
      formData.append(attribute, JSON.stringify(value));
    }
  } else {
    formData.append(attribute, value);
  }
};