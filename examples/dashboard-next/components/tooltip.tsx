'use client';
import * as React from 'react';
import { cn } from '@/lib/cn';

/* Tooltip — NOT YET SPECIFIED in the design system.
 * Popover is interactive and dismissible; a tooltip is neither. A collapsed
 * icon rail cannot work without one.
 *
 * radius-8, not the radius-14 that Menu/Popover/Toast use. Building this
 * showed the "radius follows size" rule has three tiers, not two: a 28px tall
 * bubble at radius-14 is effectively a pill. See the README. */
export function Tooltip({
  label,
  side = 'right',
  children,
}: {
  label: string;
  side?: 'right' | 'top';
  children: React.ReactNode;
}) {
  const id = React.useId();
  return (
    <span className="group/tt relative inline-flex">
      {React.isValidElement(children)
        ? React.cloneElement(children as React.ReactElement<{ 'aria-describedby'?: string }>, { 'aria-describedby': id })
        : children}
      <span
        role="tooltip"
        id={id}
        className={cn(
          'pointer-events-none absolute z-70 whitespace-nowrap rounded-8 px-2 py-1',
          'bg-popover text-popover-foreground text-xs shadow-overlay',
          'opacity-0 transition-opacity group-hover/tt:opacity-100 group-focus-within/tt:opacity-100',
          side === 'right' && 'left-full top-1/2 ml-2 -translate-y-1/2',
          side === 'top' && 'bottom-full left-1/2 mb-2 -translate-x-1/2',
        )}
      >
        {label}
      </span>
    </span>
  );
}
