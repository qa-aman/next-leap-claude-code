// C2 equality check: every key in tokens.json must appear in tailwind.config.js theme.extend
// with the same value. Run: node ux-zone/adapters/equality-check.mjs
// Exit 0 on full equality, 1 on any mismatch.

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const tokens = JSON.parse(readFileSync(join(here, "..", "tokens.json"), "utf8"));

// Load the config without executing (it's an ES module exporting default)
const cfgText = readFileSync(join(here, "tailwind.config.js"), "utf8");
const jsonMatch = cfgText.match(/export default (\{[\s\S]*\});/);
if (!jsonMatch) { console.error("could not parse tailwind.config.js"); process.exit(1); }
const cfg = JSON.parse(jsonMatch[1]);

const ext = cfg.theme.extend;
const screens = cfg.theme.screens;
const miss = [];

for (const [k, v] of Object.entries(tokens.color)) {
  if (ext.colors[`uxz-${k}`] !== v.value) miss.push(`color.${k}: tokens=${v.value} cfg=${ext.colors[`uxz-${k}`]}`);
}
for (const [k, v] of Object.entries(tokens.spacing)) {
  if (ext.spacing[`uxz-${k}`] !== v.value) miss.push(`spacing.${k}`);
}
for (const [k, v] of Object.entries(tokens.radius)) {
  if (ext.borderRadius[`uxz-${k}`] !== v.value) miss.push(`radius.${k}`);
}
for (const [k, v] of Object.entries(tokens.shadow)) {
  if (ext.boxShadow[`uxz-${k}`] !== v.value) miss.push(`shadow.${k}`);
}
for (const [k, v] of Object.entries(tokens.breakpoint)) {
  if (screens[k] !== v.value) miss.push(`breakpoint.${k}`);
}
for (const [k, v] of Object.entries(tokens.typography)) {
  if (!k.startsWith("size-")) continue;
  const tk = k.replace(/^size-/, "");
  const got = ext.fontSize[`uxz-${tk}`];
  if (!got || got[0] !== v.value || got[1].lineHeight !== v.lineHeight || String(got[1].fontWeight) !== String(v.weight)) {
    miss.push(`typography.${k}`);
  }
}

if (miss.length) {
  console.error("MISMATCHES:", miss.length);
  miss.forEach(m => console.error("  -", m));
  process.exit(1);
}
console.log("PASS, tokens.json fully reflected in tailwind.config.js");
