# frozen_string_literal: true

# Bridges the generated Ruby tokens into views.
#
# Most of a page does not need this -- Tailwind classes carry colour, radius and
# spacing straight from dist/web/tokens.css. Two places do:
#
#   * a mailer, where stylesheets are stripped and every rule must be inline
#   * anything computed server side, such as the theme-color meta tag
#
# That is the whole reason dist/ruby/f055_tokens.rb exists. A Rails app that
# only ever writes Tailwind classes never needs it.
module F055Helper
  TOKENS = F055::Tokens

  # An inline CSS declaration for a named type style: f055_style(:panel_title).
  def f055_style(name)
    TOKENS::TYPE.fetch(name).css
  end

  # A resolved colour, for inline styles and meta tags: f055_color(:background).
  def f055_color(name, mode = :light)
    TOKENS.scheme(mode).fetch(name).hex
  end

  # A control dimension: f055_control("button") => "32px".
  def f055_control(role)
    TOKENS::CONTROL.fetch(role.to_s)
  end

  # Type style plus colour, for a mailer cell.
  def f055_text(style, color: :foreground, mode: :light, extra: nil)
    # f055_style already ends in ";", so chomp before joining or the output
    # carries a doubled separator into every inline style.
    [f055_style(style).chomp(";"), "color: #{f055_color(color, mode)}", extra]
      .compact.join("; ") + ";"
  end
end
