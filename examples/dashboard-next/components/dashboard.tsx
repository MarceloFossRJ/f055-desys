'use client';
import * as React from 'react';
import { Moon, PanelLeft, Search, Sun, TrendingDown, TrendingUp } from 'lucide-react';
import { Sidebar } from '@/components/sidebar';
import { AreaChart } from '@/components/chart';
import { DataTable } from '@/components/data-table';
import { Badge, Button, Card, IconButton } from '@/components/ui';
import { streams, stats } from '@/lib/data';
import { cn } from '@/lib/cn';

const RANGES = ['Last 3 months', 'Last 30 days', 'Last 7 days'] as const;

export function Dashboard() {
  const [collapsed, setCollapsed] = React.useState(false);
  const [dark, setDark] = React.useState(false);
  const [range, setRange] = React.useState<(typeof RANGES)[number]>('Last 3 months');

  React.useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  return (
    <div className="flex h-dvh overflow-hidden">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed(true)} />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center gap-3 border-b border-border px-4">
          <IconButton label="Toggle sidebar" onClick={() => setCollapsed((c) => !c)}><PanelLeft size={16} /></IconButton>
          <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-sm">
            <span className="text-muted-foreground">Catalog</span>
            <span className="text-muted-foreground" aria-hidden="true">/</span>
            <span className="font-medium">Releases</span>
          </nav>
          <div className="ml-auto flex items-center gap-2">
            <label className="relative hidden sm:block">
              <Search size={16} className="pointer-events-none absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
              <input
                placeholder="Search releases"
                aria-label="Search releases"
                className="h-8 w-56 rounded-8 bg-input pl-8 pr-3 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset"
              />
            </label>
            <IconButton label={dark ? 'Switch to light mode' : 'Switch to dark mode'} onClick={() => setDark((d) => !d)}>
              {dark ? <Sun size={16} /> : <Moon size={16} />}
            </IconButton>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto flex max-w-[1200px] flex-col gap-6 p-4 sm:p-6">
            {/* Stat cards */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {stats.map((s) => (
                <Card key={s.label} className="flex flex-col gap-1.5 p-5">
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-sm text-muted-foreground">{s.label}</span>
                    <Badge tone="outline" className="gap-1">
                      {s.up ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                      {s.delta}
                    </Badge>
                  </div>
                  <span className="type-display">{s.value}</span>
                  <span className="flex items-center gap-1.5 text-sm font-medium">
                    {s.note}
                    {s.up ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                  </span>
                  <span className="text-sm text-muted-foreground">{s.sub}</span>
                </Card>
              ))}
            </div>

            {/* Chart */}
            <Card className="flex flex-col gap-4 p-5">
              <div className="flex flex-wrap items-start gap-3">
                <div className="flex flex-col gap-0.5">
                  <h2 className="type-card-title">Total streams</h2>
                  <p className="text-sm text-muted-foreground">Across all DSPs for the last 6 months</p>
                </div>
                {/* ButtonGroup — components/ButtonGroup */}
                <div role="group" aria-label="Time range" className="ml-auto flex items-center">
                  {RANGES.map((r, i) => (
                    <button
                      key={r}
                      onClick={() => setRange(r)}
                      aria-pressed={r === range}
                      className={cn(
                        'h-8 border border-border px-3 text-sm transition-colors cursor-pointer -ml-px first:ml-0',
                        'focus-visible:outline-none focus-visible:relative focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset',
                        i === 0 && 'rounded-l-pill',
                        i === RANGES.length - 1 && 'rounded-r-pill',
                        r === range ? 'bg-muted font-medium text-foreground' : 'bg-card text-muted-foreground hover:bg-accent hover:text-foreground',
                      )}
                    >
                      {r}
                    </button>
                  ))}
                </div>
              </div>
              <AreaChart data={streams} />
            </Card>

            <DataTable />
          </div>
        </div>
      </div>
    </div>
  );
}
