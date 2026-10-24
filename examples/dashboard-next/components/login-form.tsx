'use client';
import * as React from 'react';
import { Button } from '@/components/ui';
import { cn } from '@/lib/cn';

/* Login — modelled on shadcn's login-01, rebuilt on F055.
 *
 * The card is 384px, which is not a coincidence: it is the width the reference
 * uses for every centred panel, already recorded in Dialog, Drawer, Toast and
 * the empty state. A login card is that same object.
 *
 * There is no Google mark on the Google button. Drawing someone else's logo is
 * not ours to do, and the system has no brand-icon set; the label carries it. */
export function LoginForm({ className, ...p }: React.ComponentProps<'div'>) {
  const [error, setError] = React.useState(false);

  return (
    <div {...p} className={cn('w-full max-w-[384px]', className)}>
      <div className="flex flex-col gap-6 rounded-24 bg-card p-6 shadow-card">
        <header className="flex flex-col gap-1.5">
          {/* Named styles, not literals. `panel-title` is the system's only
              negative tracking; `prose` is its 22.75px long-form line-height.
              Both were hand-copied in six places until this screen named them. */}
          <h1 className="type-panel-title">Login to your account</h1>
          <p className="type-prose text-muted-foreground">
            Enter your email below to login to your account
          </p>
        </header>

        <form
          className="flex flex-col gap-4"
          onSubmit={(e) => { e.preventDefault(); setError(true); }}
        >
          <div className="flex flex-col gap-1.5">
            <label htmlFor="email" className="text-sm font-medium">Email</label>
            <input
              id="email" name="email" type="email" required autoComplete="email"
              placeholder="m@example.com"
              className="h-(--control-button) w-full rounded-8 bg-input px-3 text-sm
                placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2
                focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <div className="flex items-center justify-between gap-2">
              <label htmlFor="password" className="text-sm font-medium">Password</label>
              {/* No link colour in this system, so the underline carries it. */}
              <a href="#" className="text-sm text-muted-foreground underline underline-offset-4
                hover:text-foreground focus-visible:outline-none focus-visible:ring-2
                focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset rounded-5">
                Forgot your password?
              </a>
            </div>
            <input
              id="password" name="password" type="password" required autoComplete="current-password"
              aria-invalid={error || undefined}
              aria-describedby={error ? 'password-error' : undefined}
              className={cn(
                `h-(--control-button) w-full rounded-8 bg-input px-3 text-sm
                 placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2
                 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset`,
                // Ring, not tint. The system has one hue, so an invalid field keeps
                // its fill and gains an outline -- the Validation spec's rule.
                error && 'ring-1 ring-destructive',
              )}
            />
            {error && (
              <p id="password-error" className="text-sm text-destructive-text">
                That email and password do not match.
              </p>
            )}
          </div>

          <Button type="submit" variant="primary" className="w-full">Login</Button>
          <Button type="button" className="w-full">Login with Google</Button>
        </form>
      </div>

      <p className="mt-4 text-center text-sm text-muted-foreground">
        Don&apos;t have an account?{' '}
        <a href="#" className="underline underline-offset-4 hover:text-foreground rounded-5
          focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
          focus-visible:ring-offset-2 focus-visible:ring-offset-ring-offset">Sign up</a>
      </p>
    </div>
  );
}
