from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_changelog.py"


class CheckChangelogTests(unittest.TestCase):
    def run_check(self, changelog: str, *args: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            (workdir / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), *args],
                cwd=workdir,
                check=False,
                capture_output=True,
                text=True,
            )

    def run_git(self, workdir: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=workdir,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_accepts_unreleased_section(self) -> None:
        result = self.run_check(
            "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- Preview image.\n"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_extracts_matching_version_notes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            (workdir / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n## [0.1.0] - 2026-09-02\n\n"
                "### Added\n\n- First release.\n",
                encoding="utf-8",
            )
            output = workdir / "notes.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--release-version",
                    "v0.1.0",
                    "--output",
                    str(output),
                ],
                cwd=workdir,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "### Added\n\n- First release.\n")

    def test_rejects_release_without_matching_version(self) -> None:
        result = self.run_check(
            "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- Preview image.\n",
            "--release-version",
            "v0.1.0",
            "--output",
            "notes.md",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no changelog section exists", result.stderr)

    def test_rejects_relevant_change_without_changelog_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            self.run_git(workdir, "init")
            self.run_git(workdir, "config", "user.email", "test@example.invalid")
            self.run_git(workdir, "config", "user.name", "Test")
            (workdir / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- Initial entry.\n",
                encoding="utf-8",
            )
            (workdir / "linux-vconsole.toml").write_text("[colors]\n", encoding="utf-8")
            self.run_git(workdir, "add", ".")
            self.run_git(workdir, "commit", "-m", "initial")
            base = self.run_git(workdir, "rev-parse", "HEAD")
            (workdir / "linux-vconsole.toml").write_text(
                "[colors]\nvalue = 'changed'\n", encoding="utf-8"
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", base],
                cwd=workdir,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must update CHANGELOG.md", result.stderr)

    def test_accepts_relevant_change_with_unreleased_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            self.run_git(workdir, "init")
            self.run_git(workdir, "config", "user.email", "test@example.invalid")
            self.run_git(workdir, "config", "user.name", "Test")
            (workdir / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- Initial entry.\n",
                encoding="utf-8",
            )
            (workdir / "linux-vconsole.toml").write_text("[colors]\n", encoding="utf-8")
            self.run_git(workdir, "add", ".")
            self.run_git(workdir, "commit", "-m", "initial")
            base = self.run_git(workdir, "rev-parse", "HEAD")
            (workdir / "linux-vconsole.toml").write_text(
                "[colors]\nvalue = 'changed'\n", encoding="utf-8"
            )
            (workdir / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- Initial entry.\n- Changed palette.\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--base", base],
                cwd=workdir,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
