// Regenerates tailwind.config.js from tokens.json.
// Run: node ux-zone/adapters/build-tailwind.mjs
// Source of truth = tokens.json. Do not edit tailwind.config.js by hand.

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const tokens = JSON.parse(readFileSync(join(here, "..", "tokens.json"), "utf8"));

const colors = {};
for (const [k, v] of Object.entries(tokens.color)) colors[k] = v.value;

const fontFamily = {
  article: tokens.typography["family-article"].value.replace(/['"]/g, "").split(",").map(s => s.trim()),
  footer:  tokens.typography["family-footer"].value.split(",").map(s => s.trim()),
  system:  tokens.typography["family-system"].value.split(",").map(s => s.trim()),
};

const fontSize = {};
for (const [k, v] of Object.entries(tokens.typography)) {
  if (!k.startsWith("size-")) continue;
  const key = k.replace(/^size-/, "");
  fontSize[key] = [v.value, { lineHeight: v.lineHeight, fontWeight: String(v.weight) }];
  if (v.letterSpacing) fontSize[key][1].letterSpacing = v.letterSpacing;
}

const spacing = {};
for (const [k, v] of Object.entries(tokens.spacing)) spacing[k] = v.value;

const borderRadius = {};
for (const [k, v] of Object.entries(tokens.radius)) borderRadius[k] = v.value;

const boxShadow = {};
for (const [k, v] of Object.entries(tokens.shadow)) boxShadow[k] = v.value;

const screens = {};
for (const [k, v] of Object.entries(tokens.breakpoint)) screens[k] = v.value;

const config = {
  content: [
    "../components/**/*.{html,jsx}",
    "../templates/**/*.{html,jsx}",
    "../index.html",
  ],
  theme: {
    screens,
    extend: {
      colors: Object.fromEntries(Object.entries(colors).map(([k,v]) => [`uxz-${k}`, v])),
      fontFamily: {
        "uxz-article": fontFamily.article,
        "uxz-footer":  fontFamily.footer,
        "uxz-system":  fontFamily.system,
      },
      fontSize:    Object.fromEntries(Object.entries(fontSize).map(([k,v]) => [`uxz-${k}`, v])),
      spacing:     Object.fromEntries(Object.entries(spacing).map(([k,v]) => [`uxz-${k}`, v])),
      borderRadius: Object.fromEntries(Object.entries(borderRadius).map(([k,v]) => [`uxz-${k}`, v])),
      boxShadow:    Object.fromEntries(Object.entries(boxShadow).map(([k,v]) => [`uxz-${k}`, v])),
      maxWidth: { "uxz-article": tokens.layout["article-max-width"].value },
    },
  },
  plugins: [],
};

const out = `// AUTO-GENERATED from ../tokens.json by build-tailwind.mjs. Do not edit by hand.
// Run: node ux-zone/adapters/build-tailwind.mjs

/** @type {import('tailwindcss').Config} */
export default ${JSON.stringify(config, null, 2)};
`;

writeFileSync(join(here, "tailwind.config.js"), out);
console.log("wrote", join(here, "tailwind.config.js"));
