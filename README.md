# Alacritty Theme: Linux VConsole

A color scheme for Alacritty that matches the modern Linux Virtual Console (TTY) appearance.

## Why this exists

Alacritty's standard `linux.toml` theme targets legacy VGA text mode. On modern systems using DRM/KMS framebuffers (`fbcon`), the kernel renders the 16-color palette differently:

1.  **True Black Background:** Unlike many "dark" themes (including Alabaster Dark) which use slightly grey backgrounds, the native console is pure `#000000`.
2.  **Desaturated High-Intensity Colors:** Modern framebuffer drivers render "Bold" text using a high-intensity palette that appears lighter and more desaturated (similar to the Alabaster palette) than the primary VGA colors.
3.  **Bold as Color:** In the native console, bold text is often distinguished solely by its brighter color rather than an increased font weight.

## Features

- Pure black background matching UEFI/Plymouth
- Normal colors kept dark for background use
- Bright colors tuned for modern DRM drivers
- Designed for `draw_bold_text_with_bright_colors = true`

## Recommended Alacritty Configuration

To achieve the intended look, ensure your `alacritty.toml` includes:

```toml
[colors]
draw_bold_text_with_bright_colors = true

[font.bold]
family = "Px437 IBM VGA 8x16"
style = "Regular"
```

## Font Attribution

The recommended font **Px437 IBM VGA 8x16** is from [The Ultimate Oldschool PC Font Pack](https://int10h.org/oldschool-pc-fonts/) by VileR, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
