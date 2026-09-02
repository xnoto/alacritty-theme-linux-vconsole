# Repository guidance

## Scope and ownership

`xnoto/alacritty-theme-linux-vconsole` is the canonical source for the
`linux-vconsole.toml` color palette, its public documentation, and its release
history. It does not own installed Alacritty configuration or chezmoi external
mappings; those belong to [`xnoto/dotfiles`](https://github.com/xnoto/dotfiles).

Keep `linux-vconsole.toml` a palette-only file. User behavior, including
`colors.draw_bold_text_with_bright_colors`, and font selection belong in a
user's base Alacritty configuration and must be documented as recommendations,
not embedded as theme behavior.

## Change process

1. Work on a scoped branch and open a pull request against `main`.
2. For changes to `linux-vconsole.toml`, `README.md`, or `images/`, update the
   `Unreleased` section in `CHANGELOG.md` in the same change. CI enforces this.
3. Do not rename or move `linux-vconsole.toml` without first identifying and
   updating every consumer in its owning repository.
4. Never claim installation or visual verification without separate evidence.

## Release process

A GitHub Release is publication metadata, not workstation deployment. The
current chezmoi consumer tracks `main`, not a release tag.

Before requesting a release, an agent must verify all of the following:

1. The relevant CI run for the exact `main` commit succeeded.
2. `CHANGELOG.md` contains a dated `X.Y.Z` section with the intended release
   notes, moved from `Unreleased`.
3. The release tag is `vX.Y.Z` and points to that validated `main` commit.
4. The release is explicitly authorized by the owner.

Creating a `v*` tag triggers `.github/workflows/release.yml`, which verifies
that the tag points to `main`, extracts the matching changelog section, and
creates the GitHub Release. Agents must not create tags, releases, or invoke
release workflows without explicit confirmation.

After publication, report stages separately: authored, validated, published,
selected, installed, and functionally verified. Publication does not prove any
later stage.

## Safety

Treat this repository as public. Do not commit credentials, tokens, private
keys, decrypted secrets, host-specific configuration, or screenshots containing
sensitive terminal content.
