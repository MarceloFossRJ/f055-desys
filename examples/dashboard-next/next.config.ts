import path from 'node:path';
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Static export: this screen has no server data, and an `out/` folder of plain
  // HTML is what lets the design system be checked by rendering it.
  output: 'export',

  // The repo root, so app/globals.css can @import the real dist/web/tokens.css.
  // Without this Turbopack refuses the file as "outside configured roots" and
  // the example would have to vendor a copy of the tokens -- which is exactly
  // the drift this example exists to rule out.
  turbopack: { root: path.resolve(process.cwd(), '../..') },
};

export default nextConfig;
