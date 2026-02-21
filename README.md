# Alacritty Theme: Linux VConsole

A color scheme for Alacritty that provides a seamless transition from the systemd/Plymouth boot process to a terminal environment that perfectly matches the "naturally occurring" appearance of a modern Linux Virtual Console (TTY).

## Why this exists

While Alacritty's standard `linux.toml` theme targets the legacy VGA text mode palette, it fails to replicate the visual reality of modern Linux distributions. On systems using high-resolution DRM/KMS framebuffers (`fbcon`), the kernel's default 16-color palette is rendered with distinct characteristics:

1.  **True Black Background:** Unlike many "dark" themes (including Alabaster Dark) which use slightly grey backgrounds, the native console is pure `#000000`.
2.  **Desaturated High-Intensity Colors:** Modern framebuffer drivers render "Bold" text using a high-intensity palette that appears lighter and more desaturated (similar to the Alabaster palette) than the primary VGA colors.
3.  **Bold as Color:** In the native console, bold text is often distinguished solely by its brighter color rather than an increased font weight.

## Features

- **Seamless Boot Flow:** Matches the pure black background of UEFI/Plymouth BGRT splash screens.
- **Accurate `fbcon` Mapping:** Normal colors are kept dark for backgrounds (e.g., broken symlinks in `ls`), while bright colors are tuned to match the high-intensity rendering of the Intel i915 and other modern DRM drivers.
- **Color-Only Bold:** Designed to be used with a configuration that maps bold text to brighter colors without changing font weight, maintaining the classic TTY aesthetic.

## Recommended Alacritty Configuration

To achieve the intended look, ensure your `alacritty.toml` includes:

```toml
[colors]
draw_bold_text_with_bright_colors = true

[font.bold]
# Use the same family/style as your normal font to match TTY behavior
family = "Px437 IBM VGA 8x16"
style = "Regular"
```
