import * as React from 'react';
import { cn } from '@/lib/cn';

/* ---------------------------------------------------------------------------
 * Primitives built from the specs in components/<Name>/README.md.
 * Every value here is a token utility. No raw colours, no arbitrary sizes
 * except control heights, which the system has not tokenised yet.
 * ------------------------------------------------------------------------- */

/* Button — components/Button */
type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md';
};
export function Button({ variant = 'outline', size = 'md', className, ...p }: ButtonProps) {
  return (
    <button
      {...p}
      className={cn(
        'inline-flex items-center justify-center gap-1.5 rounded-pill border font-medium',
        'whitespace-nowrap transition-colors cursor-pointer',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        size === 'sm' ? 'h-7 px-3 text-sm' : 'h-8 px-4 text-sm',
        variant === 'primary' && 'border-transparent bg-primary text-primary-foreground hover:opacity-90',
        variant === 'outline' && 'border-border bg-card text-foreground shadow-thumb hover:bg-accent',
        variant === 'ghost' && 'border-transparent bg-transparent text-foreground hover:bg-accent',
        variant === 'destructive' && 'border-transparent bg-destructive text-destructive-foreground hover:opacity-90',
        className,
      )}
    />
  );
}

/* Icon-only button. The system has no size tokens, so 28/32 are literals. */
export function IconButton({ className, label, ...p }: React.ButtonHTMLAttributes<HTMLButtonElement> & { label: string }) {
  return (
    <button
      {...p}
      aria-label={label}
      className={cn(
        'inline-grid size-8 place-content-center rounded-6 text-muted-foreground cursor-pointer',
        'hover:bg-accent hover:text-foreground transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset',
        className,
      )}
    />
  );
}

/* Card — components/Card. radius-24 + shadow-card, never overlay geometry. */
export function Card({ className, ...p }: React.HTMLAttributes<HTMLDivElement>) {
  return <div {...p} className={cn('rounded-24 bg-card text-card-foreground shadow-card', className)} />;
}

/* Badge — components/Badge */
export function Badge({
  tone = 'muted',
  className,
  ...p
}: React.HTMLAttributes<HTMLSpanElement> & { tone?: 'muted' | 'outline' | 'primary' }) {
  return (
    <span
      {...p}
      className={cn(
        'inline-flex items-center gap-1 rounded-pill px-2 py-0.5 text-xs font-medium whitespace-nowrap',
        tone === 'muted' && 'bg-muted text-muted-foreground',
        tone === 'outline' && 'border border-border text-foreground',
        tone === 'primary' && 'bg-primary text-primary-foreground',
        className,
      )}
    />
  );
}

/* Avatar — components/Avatar */
export function Avatar({ initials, className }: { initials: string; className?: string }) {
  return (
    <span
      className={cn(
        'inline-grid size-8 shrink-0 place-content-center rounded-full bg-muted text-xs font-medium text-muted-foreground',
        className,
      )}
    >
      {initials}
    </span>
  );
}

/* Separator — the `hairline` elevation, used as a line rather than a ring. */
export function Separator({ className }: { className?: string }) {
  return <div role="separator" className={cn('h-px w-full bg-border', className)} />;
}
