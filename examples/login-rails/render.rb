#!/usr/bin/env ruby
# frozen_string_literal: true

# Renders the views without Rails, so they can be looked at and measured.
#
#   ruby render.rb [out_dir]
#
# rubygems is unreachable from this repo's sandbox, so Rails cannot be
# installed here. The views are real Rails views; this file supplies the few
# ActionView methods they use, and nothing more. It is a test harness, not a
# framework -- if it starts growing, that is a sign the views have drifted into
# something only Rails can render, which defeats the point.
#
# One genuine difference: Rails compiles ERB with Erubi, which supports
# `<%= form_with ... do |f| %>` by capturing the block. Stock ERB does not, so
# the source is rewritten to the `<%` form below and form_with writes its own
# tags to the buffer. The views stay authentic; the harness compensates.

require "erb"
require "cgi"
require "fileutils"
require_relative "../../dist/ruby/f055_tokens"
require_relative "app/helpers/f055_helper"

OUT = File.expand_path(ARGV[0] || "out", __dir__)
FileUtils.mkdir_p(OUT)

# --- the slice of ActionView these templates touch --------------------------
class FormBuilder
  def initialize(buf) = @buf = buf

  def label(name, text, class: nil, **)
    %(<label for="#{name}" class="#{binding.local_variable_get(:class)}">#{text}</label>)
  end

  def email_field(name, **opts)    = input("email", name, **opts)
  def password_field(name, **opts) = input("password", name, **opts)

  def button(text, type: "submit", class: nil, **)
    %(<button type="#{type}" name="button" class="#{binding.local_variable_get(:class)}">#{text}</button>)
  end

  private

  def input(type, name, required: false, autocomplete: nil, placeholder: nil, class: nil, **rest)
    attrs = {
      "type" => type, "name" => name.to_s, "id" => name.to_s,
      "class" => binding.local_variable_get(:class),
      "autocomplete" => autocomplete, "placeholder" => placeholder,
    }.merge(rest.transform_keys(&:to_s))
    attrs["required"] = "required" if required
    "<input " + attrs.compact.map { |k, v| %(#{k}="#{CGI.escapeHTML(v.to_s)}") }.join(" ") + " />"
  end
end

class View
  include F055Helper

  attr_reader :theme

  def initialize(theme:, assigns: {})
    @theme = theme
    @content_for = {}
    assigns.each { |k, v| instance_variable_set("@#{k}", v) }
  end

  def login_path = "/login"
  def root_path  = "/"

  def content_for(key, value = nil)
    value ? (@content_for[key] = value) : @content_for[key]
  end

  def link_to(text, href, class: nil, **)
    %(<a href="#{href}" class="#{binding.local_variable_get(:class)}">#{text}</a>)
  end

  def form_with(url:, method: :post, class: nil, **)
    @_buf << %(<form action="#{url}" method="#{method}" class="#{binding.local_variable_get(:class)}">)
    yield FormBuilder.new(@_buf)
    @_buf << "</form>"
    nil
  end

  # Erubi supports `<%= expr do |x| %>`; stock ERB does not. Rewrite those tags
  # to the statement form, which stock ERB handles, and let form_with buffer.
  BLOCK_TAG = /<%=(\s*\w+[^%]*?\sdo\s*(?:\|[^|]*\|)?\s*)%>/m

  def render(template)
    src = File.read(File.expand_path(template, __dir__)).gsub(BLOCK_TAG) { "<%#{$1}%>" }
    @_buf = +""
    # eoutvar: ERB must append to the SAME buffer form_with writes to, or the
    # form tags land in a buffer nobody returns and the <form> silently
    # disappears -- which is exactly what happened the first time.
    ERB.new(src, trim_mode: "-", eoutvar: "@_buf").result(binding)
  end

  def render_with_layout(template, layout: "app/views/layouts/application.html.erb")
    body = render(template)
    @_yield = body
    # `yield` is a keyword, so a method of that name is never reached. Rewrite
    # the layout's `<%= yield %>` the same way the block tags are rewritten:
    # the view stays authentic, the harness compensates.
    src = File.read(File.expand_path(layout, __dir__))
             .gsub(/<%=\s*yield\s*%>/, "<%= @_yield %>")
    ERB.new(src, trim_mode: "-").result(binding)
  end
end

# --- render -----------------------------------------------------------------
%w[light dark].each do |theme|
  %w[false true].each do |err|
    v = View.new(theme: theme, assigns: { error: err == "true" })
    html = v.render_with_layout("app/views/sessions/new.html.erb")
    name = err == "true" ? "login-#{theme}-error.html" : "login-#{theme}.html"
    File.write(File.join(OUT, name), html)
    puts format("%-26s %6d bytes", name, html.bytesize)
  end
end

mail = View.new(theme: "light",
                assigns: { email: "marcelo@f055.dev", url: "https://f055.dev/reset/abc123" })
html = mail.render("app/views/user_mailer/password_reset.html.erb")
File.write(File.join(OUT, "password-reset-email.html"), html)
puts format("%-26s %6d bytes", "password-reset-email.html", html.bytesize)

FileUtils.cp_r(File.expand_path("public/assets", __dir__), OUT) rescue nil
puts "assets copied -> #{OUT}"
