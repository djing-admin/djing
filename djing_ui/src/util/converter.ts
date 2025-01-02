export interface BrandColors {
  [key: string]: string;
}

export const convertBrandColorsToCSSVariables = (
  brandColors: BrandColors
): any => {
  let rootStyles = ":root {\n";

  Object.entries(brandColors).forEach(([key, value]) => {
    const rgbaColor = value.replace(/,/g, ",");

    rootStyles += `  --colors-primary-${key}: ${rgbaColor};\n`;
  });

  rootStyles += "}\n";

  return rootStyles
};
