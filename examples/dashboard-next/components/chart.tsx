'use client';
import * as React from 'react';
import { cn } from '@/lib/cn';

/* Chart — NOT YET SPECIFIED in the design system.
 *
 * Two series, so two CATEGORICAL slots: series-1 (the brand red) and series-3
 * (muted ink). Not chart-1..5 — that is the SEQUENTIAL ramp, for magnitude.
 * Building this screen is what split the two families apart: measured against
 * 3:1, the old theme-invariant ramp left chart-1 at 1.87:1 on light and
 * chart-4/5 at 2.71 and 2.08 on dark, so five tokens yielded one usable mark.
 *
 * series-3 is the same value as muted-foreground, which the axis labels also
 * wear, so it carries a DISTINCT MARK TYPE — a dashed line against a filled
 * area. The token's own note requires this; identity never rests on hue here.
 *
 * Hand-built SVG rather than a chart library so every value is a token. A
 * library adapter is the obvious follow-up; it is not what this proves. */

export type Point = { label: string; current: number; previous: number };

const W = 720, H = 240, PAD_L = 44, PAD_R = 8, PAD_T = 12, PAD_B = 28;
// Geometry is the chart's own, not control sizing -- no size token applies.

function niceMax(v: number) {
  const mag = 10 ** Math.floor(Math.log10(v));
  return Math.ceil(v / (mag / 2)) * (mag / 2);
}
const fmt = (n: number) => (n >= 1000 ? `${(n / 1000).toFixed(n % 1000 === 0 ? 0 : 1)}k` : `${n}`);

export function AreaChart({ data, unit = 'streams' }: { data: Point[]; unit?: string }) {
  const [hover, setHover] = React.useState<number | null>(null);
  const svgRef = React.useRef<SVGSVGElement>(null);

  const max = niceMax(Math.max(...data.flatMap((d) => [d.current, d.previous])));
  const innerW = W - PAD_L - PAD_R, innerH = H - PAD_T - PAD_B;
  const x = (i: number) => PAD_L + (i / (data.length - 1)) * innerW;
  const y = (v: number) => PAD_T + innerH - (v / max) * innerH;

  const line = (key: 'current' | 'previous') => data.map((d, i) => `${i ? 'L' : 'M'}${x(i)},${y(d[key])}`).join(' ');
  const area = `${line('current')} L${x(data.length - 1)},${PAD_T + innerH} L${PAD_L},${PAD_T + innerH} Z`;
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((t) => t * max);

  function onMove(e: React.PointerEvent) {
    const r = svgRef.current?.getBoundingClientRect();
    if (!r) return;
    const px = ((e.clientX - r.left) / r.width) * W;
    const i = Math.round(((px - PAD_L) / innerW) * (data.length - 1));
    setHover(i >= 0 && i < data.length ? i : null);
  }

  const active = hover === null ? null : data[hover];

  return (
    <div className="relative">
      <svg
        ref={svgRef}
        viewBox={`0 0 ${W} ${H}`}
        className="w-full"
        role="img"
        aria-label={`${unit} this period compared with the previous period`}
        onPointerMove={onMove}
        onPointerLeave={() => setHover(null)}
      >
        <defs>
          <linearGradient id="f055-area" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--series-1)" stopOpacity="0.28" />
            <stop offset="100%" stopColor="var(--series-1)" stopOpacity="0.02" />
          </linearGradient>
        </defs>

        {/* Grid and axis: recessive, in border/muted ink, never the series colour */}
        {ticks.map((t) => (
          <g key={t}>
            <line x1={PAD_L} x2={W - PAD_R} y1={y(t)} y2={y(t)} stroke="var(--border)" strokeWidth={1} vectorEffect="non-scaling-stroke" />
            <text x={PAD_L - 8} y={y(t) + 4} textAnchor="end" className="fill-muted-foreground text-xs" style={{ fontSize: 12 }}>
              {fmt(t)}
            </text>
          </g>
        ))}
        {data.map((d, i) => (
          <text key={d.label} x={x(i)} y={H - 8} textAnchor="middle" className="fill-muted-foreground text-xs" style={{ fontSize: 12 }}>
            {d.label}
          </text>
        ))}

        {/* Previous period: dashed neutral line. Different mark type, not just a
            different colour -- the identity does not rest on hue alone. */}
        <path d={line('previous')} fill="none" stroke="var(--series-3)" strokeWidth={2} strokeDasharray="4 4" strokeLinecap="round" vectorEffect="non-scaling-stroke" />

        {/* Current period */}
        <path d={area} fill="url(#f055-area)" />
        <path d={line('current')} fill="none" stroke="var(--series-1)" strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" vectorEffect="non-scaling-stroke" />

        {active && hover !== null && (
          <g>
            <line x1={x(hover)} x2={x(hover)} y1={PAD_T} y2={PAD_T + innerH} stroke="var(--border)" strokeWidth={1} vectorEffect="non-scaling-stroke" />
            <circle cx={x(hover)} cy={y(active.previous)} r={4} fill="var(--card)" stroke="var(--series-3)" strokeWidth={2} vectorEffect="non-scaling-stroke" />
            <circle cx={x(hover)} cy={y(active.current)} r={4} fill="var(--card)" stroke="var(--series-1)" strokeWidth={2} vectorEffect="non-scaling-stroke" />
          </g>
        )}
      </svg>

      {/* Tooltip — popover shell, radius-8 like Tooltip rather than radius-14 */}
      {active && hover !== null && (
        <div
          className="pointer-events-none absolute top-2 rounded-8 bg-popover px-3 py-2 shadow-overlay"
          style={{ left: `calc(${(x(hover) / W) * 100}% + 8px)` }}
          role="status"
        >
          <div className="text-xs font-medium">{active.label}</div>
          <Row swatch="bg-series-1" label="This period" value={active.current.toLocaleString('en-US')} />
          <Row swatch="bg-series-3" label="Previous" value={active.previous.toLocaleString('en-US')} />
        </div>
      )}

      <Legend />
    </div>
  );
}

function Row({ swatch, label, value }: { swatch: string; label: string; value: string }) {
  return (
    <div className="flex items-center gap-2 whitespace-nowrap text-xs">
      <span className={cn('size-2 rounded-full', swatch)} />
      <span className="text-muted-foreground">{label}</span>
      <span className="ml-auto font-mono tabular-nums">{value}</span>
    </div>
  );
}

/* Two series, so a legend is always present. */
function Legend() {
  return (
    <div className="mt-2 flex items-center gap-4 pl-11">
      <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
        <svg width="16" height="8" aria-hidden="true"><line x1="0" y1="4" x2="16" y2="4" stroke="var(--series-1)" strokeWidth="2" strokeLinecap="round" /></svg>
        This period
      </span>
      <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
        <svg width="16" height="8" aria-hidden="true"><line x1="0" y1="4" x2="16" y2="4" stroke="var(--series-3)" strokeWidth="2" strokeDasharray="4 4" strokeLinecap="round" /></svg>
        Previous period
      </span>
    </div>
  );
}
