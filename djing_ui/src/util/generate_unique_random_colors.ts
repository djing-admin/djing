export const generate_unique_random_colors = (count: number): string[] => {
  const colors: Set<string> = new Set();

  while (colors.size < count) {
    const color = `#${Math.floor(Math.random() * 0xffffff)
      .toString(16)
      .padStart(6, "0")}`;

    colors.add(color);
  }

  return Array.from(colors);
};