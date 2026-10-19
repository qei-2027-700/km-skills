import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SKILLS = sorted(path for path in (REPO / "skills").iterdir() if (path / "SKILL.md").is_file())


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="km-skills-test-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.claude = self.home / ".claude/skills"
        self.codex = self.home / ".agents/skills"

    def install(self, *args):
        return subprocess.run(
            ["bash", str(REPO / "install.sh"), *args],
            env={**os.environ, "HOME": str(self.home)},
            cwd=self.home,
            capture_output=True,
            text=True,
        )

    def assert_links(self, directory):
        for skill in SKILLS:
            link = directory / skill.name
            self.assertTrue(link.is_symlink(), str(link))
            self.assertEqual(link.resolve(), skill.resolve())
            self.assertEqual((link / "SKILL.md").read_bytes(), (skill / "SKILL.md").read_bytes())

    def test_default_installs_both_and_can_repeat(self):
        for _ in range(2):
            self.assertEqual(self.install().returncode, 0)
            self.assert_links(self.claude)
            self.assert_links(self.codex)

    def test_explicit_all(self):
        self.assertEqual(self.install("all").returncode, 0)
        self.assert_links(self.claude)
        self.assert_links(self.codex)

    def test_individual_targets(self):
        self.assertEqual(self.install("codex").returncode, 0)
        self.assert_links(self.codex)
        self.assertFalse(self.claude.exists())
        self.assertEqual(self.install("claude").returncode, 0)
        self.assert_links(self.claude)

    def test_preserves_existing_directory_and_file(self):
        self.claude.mkdir(parents=True)
        existing = self.claude / SKILLS[0].name
        existing.mkdir()
        marker = existing / "keep.txt"
        marker.write_text("keep directory")
        other = self.claude / SKILLS[1].name
        other.write_text("keep file")
        result = self.install()
        self.assertEqual(result.returncode, 0)
        self.assertIn("skip", result.stdout)
        self.assertEqual(marker.read_text(), "keep directory")
        self.assertEqual(other.read_text(), "keep file")
        self.assert_links(self.codex)

    def test_replaces_broken_symlink(self):
        self.codex.mkdir(parents=True)
        (self.codex / SKILLS[0].name).symlink_to(self.home / "missing")
        self.assertEqual(self.install("codex").returncode, 0)
        self.assert_links(self.codex)

    def test_invalid_arguments_do_not_install(self):
        for args in [("invalid",), ("codex", "extra")]:
            self.assertNotEqual(self.install(*args).returncode, 0)
        self.assertFalse(self.claude.exists())
        self.assertFalse(self.codex.exists())

    def test_help_does_not_install(self):
        result = self.install("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)
        self.assertFalse(self.claude.exists())
        self.assertFalse(self.codex.exists())


if __name__ == "__main__":
    unittest.main()
