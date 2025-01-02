export const title_to_slug_case = (title: string): string => {
  return title
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '-');
};