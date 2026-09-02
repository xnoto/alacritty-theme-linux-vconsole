# Alacritty Theme: Linux VConsole

A color scheme for Alacritty inspired by the modern Linux Virtual Console (TTY)
appearance on DRM/KMS framebuffer systems (`fbcon`).

It is distinct from Alacritty's upstream
[`linux.toml`](https://github.com/alacritty/alacritty-theme/blob/master/themes/linux.toml),
which targets the legacy VGA console palette. This theme is deliberately tuned
to approximate the modern framebuffer-console appearance; it does not assert a
single, universal kernel-rendered palette.

## Why this exists

1. **True black background:** The native console is pure `#000000`, unlike
   dark themes that use a slightly grey background.
2. **Desaturated high-intensity colors:** The bright palette is tuned toward
   the lighter, less saturated appearance commonly associated with modern
   framebuffer consoles.
3. **Bright bold text:** Linux console-like output commonly distinguishes bold
   text with the bright palette rather than a heavier font weight.

## Features

- Pure black background intended to match UEFI/Plymouth styling
- Dark normal colors for background use
- Bright colors tuned for a modern framebuffer-console-inspired appearance
- A standalone color palette that does not change application behavior or font
  selection when imported

## Installation

1. Download the `linux-vconsole.toml` file to your Alacritty configuration
   directory (usually `~/.config/alacritty/` on Linux/macOS or
   `%APPDATA%\\alacritty\\` on Windows).
2. Open your main `alacritty.toml` file and add the import statement:

```toml
[general]
import = [
    "~/.config/alacritty/linux-vconsole.toml"
]
```

## Recommended Alacritty configuration

This theme supplies **color values only**. It intentionally does not set
`colors.draw_bold_text_with_bright_colors`, because that is a user-level
behavior choice rather than part of the palette.

To reproduce the intended virtual-console-inspired bright-bold behavior, add
the following to your base `alacritty.toml` configuration:

```toml
[colors]
draw_bold_text_with_bright_colors = true
```

This setting is recommended, not required: the color palette remains usable
without it, but bold text will not automatically use the bright color variants.

The following font configuration is also optional, but complements the intended
look:

```toml
[font.bold]
family = "Px437 IBM VGA 8x16"
style = "Regular"
```

## Font Attribution

The recommended font **Px437 IBM VGA 8x16** is from [The Ultimate Oldschool PC
Font Pack](https://int10h.org/oldschool-pc-fonts/) by VileR, licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Development

Run `pre-commit run --all-files` before submitting changes. When refreshing
hooks, freeze any mutable release channel such as Typos' `v1` tag to its commit
SHA; pre-commit does not support moving references reliably.
