'use client';
import * as React from 'react';
import {
  AudioLines, BarChart3, Boxes, ChevronsLeft, CircleHelp, Disc3, FileText,
  Inbox, LayoutDashboard, type LucideIcon, Plus, Receipt, Settings, SlidersHorizontal, Split, Users,
} from 'lucide-react';
import { Avatar, Separator } from '@/components/ui';
import { Tooltip } from '@/components/tooltip';
import { cn } from '@/lib/cn';

/* Sidebar — NOT YET SPECIFIED in the design system.
 * Nav is a vertical item list and NavBar is a horizontal top bar; neither is
 * the app shell. What is new here: groups with labels, a collapsed icon rail,
 * a footer identity block, and the rail/label swap.
 *
 * Active state is `muted`, never `primary` -- current location is muted, a
 * chosen value is primary (CLAUDE.md). */

type Item = { label: string; icon: LucideIcon; active?: boolean };

const MAIN: Item[] = [
  { label: 'Dashboard', icon: LayoutDashboard },
  { label: 'Releases', icon: Disc3, active: true },
  { label: 'Analytics', icon: BarChart3 },
  { label: 'Royalties', icon: Receipt },
  { label: 'Catalog', icon: Boxes },
  { label: 'Team', icon: Users },
];
const LIBRARY: Item[] = [
  { label: 'Masters', icon: AudioLines },
  { label: 'Reports', icon: FileText },
  { label: 'Splits', icon: Split },
];
const FOOTER: Item[] = [
  { label: 'Settings', icon: Settings },
  { label: 'Get Help', icon: CircleHelp },
];

function Row({ item, collapsed }: { item: Item; collapsed: boolean }) {
  const Icon = item.icon;
  const btn = (
    <button
      aria-current={item.active ? 'page' : undefined}
      className={cn(
        'flex h-8 w-full items-center gap-2 rounded-6 px-2 text-sm transition-colors cursor-pointer',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset',
        collapsed && 'justify-center px-0',
        item.active ? 'bg-muted font-medium text-foreground' : 'text-muted-foreground hover:bg-accent hover:text-foreground',
      )}
    >
      <Icon size={16} className="shrink-0" />
      {!collapsed && <span className="truncate">{item.label}</span>}
    </button>
  );
  // Collapsed to a rail, the label is gone -- a tooltip is the only thing
  // carrying it, which is why Tooltip had to exist before Sidebar could.
  return collapsed ? <Tooltip label={item.label}>{btn}</Tooltip> : btn;
}

function Group({ label, items, collapsed }: { label?: string; items: Item[]; collapsed: boolean }) {
  return (
    <div className="flex flex-col gap-0.5">
      {label && !collapsed && (
        <div className="px-2 pb-1 pt-3 text-xs font-medium text-muted-foreground">{label}</div>
      )}
      {label && collapsed && <Separator className="my-2" />}
      {items.map((i) => (
        <Row key={i.label} item={i} collapsed={collapsed} />
      ))}
    </div>
  );
}

export function Sidebar({ collapsed, onToggle }: { collapsed: boolean; onToggle: () => void }) {
  return (
    <aside
      className={cn(
        'flex shrink-0 flex-col border-r border-border bg-card transition-[width] duration-200',
        collapsed ? 'w-14' : 'w-64',
      )}
    >
      <div className={cn('flex h-14 items-center gap-2 px-3', collapsed && 'justify-center px-0')}>
        <span className="grid size-8 shrink-0 place-content-center rounded-8 bg-primary text-primary-foreground">
          <AudioLines size={16} />
        </span>
        {!collapsed && (
          <>
            <span className="flex-1 truncate text-sm font-medium">F055 Records</span>
            <button
              onClick={onToggle}
              aria-label="Collapse sidebar"
              className="grid size-8 place-content-center rounded-6 text-muted-foreground hover:bg-accent hover:text-foreground cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset"
            >
              <ChevronsLeft size={16} />
            </button>
          </>
        )}
      </div>

      <div className="flex flex-1 flex-col gap-0.5 overflow-y-auto px-2 pb-2">
        <Row item={{ label: 'Quick Create', icon: Plus }} collapsed={collapsed} />
        <Row item={{ label: 'Inbox', icon: Inbox }} collapsed={collapsed} />
        <Separator className="my-2" />
        <Group items={MAIN} collapsed={collapsed} />
        <Group label="Library" items={LIBRARY} collapsed={collapsed} />
        <div className="flex-1" />
        <Group items={FOOTER} collapsed={collapsed} />
      </div>

      <Separator />
      <div className={cn('flex items-center gap-2 p-2', collapsed && 'justify-center')}>
        <Avatar initials="MF" />
        {!collapsed && (
          <span className="flex min-w-0 flex-col">
            <span className="truncate text-sm font-medium">Marcelo Foss</span>
            <span className="truncate text-xs text-muted-foreground">marcelo@f055.dev</span>
          </span>
        )}
        {!collapsed && <SlidersHorizontal size={16} className="ml-auto shrink-0 text-muted-foreground" />}
      </div>
    </aside>
  );
}
