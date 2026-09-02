# Contributing

## Scope

Contributions should keep `linux-vconsole.toml` a standalone color palette.
Behavioral settings and font choices belong in a user's Alacritty configuration,
not in the imported theme file.

## Required pull-request content

For changes to `linux-vconsole.toml`, `README.md`, or `images/`:

1. Update `CHANGELOG.md` under `Unreleased`.
2. Explain whether the visual palette changes and how it differs from
   upstream's legacy-VGA `linux.toml` when relevant.
3. Include a non-sensitive preview image when adding a theme for distribution.

CI validates the changelog rule and repository formatting. A passing check
validates source content only; it does not install the theme or prove its visual
appearance on a workstation.

## Releases

Versioned GitHub Releases are created only from `vX.Y.Z` tags after the matching
`main` commit has passed CI and its release notes are present in
`CHANGELOG.md`. Move the intended notes out of `Unreleased` into a dated version
section before requesting a tag.

The tag-triggered release workflow publishes GitHub Release metadata only. The
chezmoi external currently follows `main`, so a release does not select, install,
or verify a workstation version. See `AGENTS.md` for the agent-specific release
and safety rules.
