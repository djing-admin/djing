export const get_colspan = (width: string) => {
  if (width == "1/2") {
    return `md:col-span-6`;
  }

  if (width == "1/3") {
    return `md:col-span-4`;
  }

  if (width == "1/4") {
    return `md:col-span-3`;
  }

  if (width == "2/3") {
    return `md:col-span-8`;
  }

  if (width == "3/4") {
    return `md:col-span-9`;
  }

  if (width == "full") {
    return `md:col-span-12`;
  }

  return `md:col-span-1`;
};