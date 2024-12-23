export const slug_to_title_case = (slug: string): string => {
  const words = slug.split('-');

  return words.map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}