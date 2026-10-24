# Login — Ruby on Rails

The same login screen as `examples/dashboard-next` and `examples/dashboard-jinja`,
plus the password-reset mailer that goes with it.

```sh
npm install && npm run build     # Tailwind + fonts, as cssbundling-rails does
ruby render.rb out               # both themes, the error state, and the email
```

## Rails is not installed here, and that is the interesting part

rubygems is unreachable from this repo's sandbox, so `bundle install` cannot
run. The views are nonetheless **real Rails views** — `form_with`, `f.label`,
`link_to`, `content_for`, a layout with `yield` — and `render.rb` supplies the
handful of ActionView methods they use so the output can still be rendered,
looked at, and measured by `scripts/check_contrast.py`.

That harness is a test fixture, not a framework. If it starts growing, the views
have drifted into something only Rails can render, which defeats the point.

Two places where stock ERB and Rails genuinely differ, both handled by rewriting
the template source rather than by making the views unrealistic:

| Rails | Stock ERB | What `render.rb` does |
|---|---|---|
| Erubi captures `<%= form_with … do \|f\| %>` | stock ERB cannot | rewrites the tag to `<% … %>`; `form_with` writes its own tags to the buffer |
| `yield` is a template method | `yield` is a keyword, so a method of that name is unreachable | rewrites `<%= yield %>` to the captured body |

The first attempt at the second one also got the buffer wrong: `form_with` wrote
to its own string while ERB wrote to another, so the `<form>` tag silently
vanished and the page still rendered. `eoutvar:` fixed it. Both buffers looked
fine in isolation; only parsing the output showed the form was gone.

## Where the generated Ruby tokens earn their place

Most of this page does not need them. Colour, radius and spacing arrive as
Tailwind classes compiled straight from `dist/web/tokens.css`, exactly as in the
other two stacks. `dist/ruby/f055_tokens.rb` is load-bearing in two places:

**The mailer.** Email clients strip `<style>`, so every rule has to be inline.
There is no Tailwind in an email and no stylesheet to link.
`app/views/user_mailer/password_reset.html.erb` builds every declaration from
the token file through `F055Helper#f055_text`, which is the only way the email
and the web app stay in step. This is what `TextStyle#css` was written for.

**`theme-color`.** The browser chrome colour is a meta tag; it cannot come from
a stylesheet, so the layout computes it with `f055_color(:background, theme)`.

A Rails app that only ever writes Tailwind classes never needs the Ruby output
at all. That is worth saying plainly rather than inventing uses for it.

## What building this exposed

**The font stacks were not safe inside an HTML attribute.** They were
double-quoted — `"Roboto", system-ui, sans-serif` — and an inline style sits
inside a double-quoted `style="…"`, so the attribute terminated at the first
quote and the entire declaration was discarded. The mailer rendered with no
typography at all.

Rails would have hidden this: `<%= %>` escapes by default, so `"` becomes
`&quot;` and it survives in a view. Nothing else escapes — not a PDF renderer,
not a mail library building MIME parts by hand, not this harness. The stacks are
single-quoted now, which is equally valid CSS and safe everywhere.

**`f055_text` doubled its separator**, because `TextStyle#css` already ends in
`;`. Cosmetic, but it was in every inline style in the email.

## Accessibility

The password field carries `aria-invalid` and `aria-describedby` when the form
comes back with an error, and the message is tied to it by id. The error state
uses a **ring, not a tint** — the system has one hue, so an invalid field keeps
its fill and gains an outline, which is the Validation spec's rule.

`f.button`, not `f.submit`: `f.submit` emits `<input type="submit">`, whose
label lives in an attribute where neither a screen reader's control list nor
`check_contrast.py` can reach it.

The controller returns one message for a bad email and a bad password alike.
Telling someone the email exists but the password is wrong confirms the account
to anyone who asks.

There is no Google mark on the Google button. Drawing someone else's logo is not
ours to do, and this system has no brand-icon set; the label carries it.
