'use client';
import * as React from 'react';
import { ChevronLeft, ChevronRight, Columns3, EllipsisVertical, GripVertical, Plus } from 'lucide-react';
import { Badge, Button, IconButton } from '@/components/ui';
import { Checkbox } from '@/components/checkbox';
import { releases, type Release, type Status } from '@/lib/data';
import { ICON } from '@/lib/tokens';
import { cn } from '@/lib/cn';

const TABS = ['All releases', 'In review', 'Scheduled', 'Takedowns'] as const;

/* Status has no palette: the system has no success green and no amber, so a
 * status cell cannot carry meaning in a fill. Only Takedown gets the one
 * accent the system has, and every status is spelled out in words. */
function StatusCell({ status }: { status: Status }) {
  if (status === 'Takedown') {
    return (
      <span className="inline-flex items-center gap-1.5 text-sm text-destructive-text">
        <span className="size-(--control-dot) rounded-full bg-destructive" aria-hidden="true" />
        Takedown
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
      <span className={cn('size-(--control-dot) rounded-full', status === 'Live' ? 'bg-foreground' : 'bg-muted-foreground')} aria-hidden="true" />
      {status}
    </span>
  );
}

export function DataTable() {
  const [tab, setTab] = React.useState<(typeof TABS)[number]>('All releases');
  const [selected, setSelected] = React.useState<Set<string>>(new Set(['F055-0141']));

  const rows = releases.filter((r) =>
    tab === 'All releases' ? true
      : tab === 'In review' ? r.status === 'In review'
      : tab === 'Scheduled' ? r.status === 'Scheduled'
      : r.status === 'Takedown',
  );
  const allOn = rows.length > 0 && rows.every((r) => selected.has(r.id));
  const someOn = rows.some((r) => selected.has(r.id)) && !allOn;

  function toggle(id: string) {
    setSelected((s) => { const n = new Set(s); n.has(id) ? n.delete(id) : n.add(id); return n; });
  }

  return (
    <section className="flex flex-col gap-4">
      {/* Tabs — components/Tabs. Active tab is `muted`, not `primary`. */}
      <div className="flex flex-wrap items-center gap-2">
        {/* The strip sits on `card`, not on `muted` -- muted-foreground on muted is
            4.35:1 in light, under AA. On card it is 4.74:1, and the selected tab can
            then be the muted one, which is the system's own rule for current location. */}
        <div role="tablist" className="flex items-center gap-1 rounded-10 border border-border bg-card p-1">
          {TABS.map((t) => (
            <button
              key={t}
              role="tab"
              aria-selected={t === tab}
              onClick={() => setTab(t)}
              className={cn(
                'h-(--control-button-sm) rounded-6 px-3 text-sm transition-colors cursor-pointer',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset',
                t === tab ? 'bg-muted font-medium text-foreground' : 'text-muted-foreground hover:text-foreground',
              )}
            >
              {t}
            </button>
          ))}
        </div>
        <div className="ml-auto flex items-center gap-2">
          <Button size="sm"><Columns3 size={ICON.md} />Columns</Button>
          <Button size="sm" variant="primary"><Plus size={ICON.md} />New release</Button>
        </div>
      </div>

      {/* Table — components/Table. Rows separated by hairlines, not by space. */}
      <div className="overflow-hidden rounded-24 bg-card shadow-card">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-border">
                <Th className="w-10 pl-4"><span className="sr-only">Reorder</span></Th>
                <Th className="w-10">
                  <Checkbox
                    checked={allOn}
                    indeterminate={someOn}
                    label="Select all rows"
                    onChange={(n) => setSelected(n ? new Set(rows.map((r) => r.id)) : new Set())}
                  />
                </Th>
                <Th>Release</Th>
                <Th>Type</Th>
                <Th>Status</Th>
                <Th className="text-right">Streams</Th>
                <Th className="text-right">Royalties</Th>
                <Th>Reviewer</Th>
                <Th className="w-12 pr-4"><span className="sr-only">Actions</span></Th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <Row key={r.id} r={r} on={selected.has(r.id)} toggle={() => toggle(r.id)} />
              ))}
              {rows.length === 0 && (
                <tr><td colSpan={9} className="px-4 py-12 text-center text-sm text-muted-foreground">No releases in this view.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination — components/Pagination */}
      <div className="flex flex-wrap items-center gap-4">
        <span className="text-sm text-muted-foreground">
          {selected.size} of {rows.length} row(s) selected.
        </span>
        <div className="ml-auto flex items-center gap-4">
          <label className="flex items-center gap-2 text-sm">
            <span className="text-muted-foreground">Rows per page</span>
            <select
              defaultValue="8"
              className="h-(--control-button) rounded-8 border border-border bg-card px-2 text-sm cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset"
            >
              <option>8</option><option>16</option><option>32</option>
            </select>
          </label>
          <span className="text-sm text-muted-foreground">Page 1 of 7</span>
          <div className="flex items-center gap-1">
            <IconButton label="Go to previous page" disabled className="opacity-50"><ChevronLeft size={ICON.md} /></IconButton>
            <IconButton label="Go to next page"><ChevronRight size={ICON.md} /></IconButton>
          </div>
        </div>
      </div>
    </section>
  );
}

function Th({ className, children }: { className?: string; children: React.ReactNode }) {
  return <th scope="col" className={cn('px-3 py-2.5 text-left text-xs font-medium text-muted-foreground', className)}>{children}</th>;
}

function Row({ r, on, toggle }: { r: Release; on: boolean; toggle: () => void }) {
  return (
    <tr className={cn('border-b border-border last:border-0 transition-colors', on ? 'bg-muted-subtle' : 'hover:bg-muted-subtle')}>
      <td className="pl-4 text-muted-foreground"><GripVertical size={ICON.md} aria-label="Drag to reorder" /></td>
      <td><Checkbox checked={on} onChange={toggle} label={`Select ${r.title}`} /></td>
      <td className="px-3 py-2.5">
        <div className="font-medium">{r.title}</div>
        <div className="text-xs text-muted-foreground">{r.artist} · <span className="font-mono">{r.id}</span></div>
      </td>
      <td className="px-3 py-2.5"><Badge tone="outline">{r.type}</Badge></td>
      <td className="px-3 py-2.5"><StatusCell status={r.status} /></td>
      <td className="px-3 py-2.5 text-right font-mono tabular-nums">{r.streams ? r.streams.toLocaleString('en-US') : '—'}</td>
      <td className="px-3 py-2.5 text-right font-mono tabular-nums">{r.royalties ? `€${r.royalties.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '—'}</td>
      <td className="px-3 py-2.5">
        {r.reviewer ?? <Button size="sm" variant="ghost" className="px-2 text-muted-foreground">Assign reviewer</Button>}
      </td>
      <td className="pr-4"><IconButton label={`Open menu for ${r.title}`}><EllipsisVertical size={ICON.md} /></IconButton></td>
    </tr>
  );
}
