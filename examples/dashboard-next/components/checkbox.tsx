'use client';
import * as React from 'react';
import { Check, Minus } from 'lucide-react';
import { ICON } from '@/lib/tokens';
import { cn } from '@/lib/cn';

/* Checkbox — NOT YET SPECIFIED in the design system.
 * Toggle is a switch; Menu has a checkbox *item*. This is the standalone box,
 * needed for table-row selection. Built here first; the spec follows from it.
 *
 * --control-checkbox at radius-5 (the smallest radius the system has). Unchecked uses the
 * `track` token, same as an unchecked Toggle -- that is what `track` is for. */
export function Checkbox({
  checked,
  indeterminate,
  onChange,
  label,
  className,
}: {
  checked: boolean;
  indeterminate?: boolean;
  onChange: (next: boolean) => void;
  label: string;
  className?: string;
}) {
  const on = checked || !!indeterminate;
  return (
    <button
      type="button"
      role="checkbox"
      aria-checked={indeterminate ? 'mixed' : checked}
      aria-label={label}
      onClick={() => onChange(!checked)}
      className={cn(
        'inline-grid size-(--control-checkbox) shrink-0 place-content-center rounded-5 border transition-colors cursor-pointer',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset',
        // `border` is 1.26:1 against a light row -- the control vanishes, which fails
        // WCAG 1.4.11. `border-strong` exists for exactly this: the outline of a control
        // a person has to see in order to operate it.
        on ? 'border-transparent bg-primary text-primary-foreground' : 'border-border-strong bg-track',
        className,
      )}
    >
      {indeterminate ? <Minus size={ICON.xs} strokeWidth={3} /> : checked ? <Check size={ICON.xs} strokeWidth={3} /> : null}
    </button>
  );
}
