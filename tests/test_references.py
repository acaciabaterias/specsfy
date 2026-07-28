from __future__ import annotations

import json
import re
import struct
import unittest
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "vendor",
}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+[^)]*)?\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+]:\s*(\S+)", re.MULTILINE)
HTML_ASSET = re.compile(
    r"\b(?:href|src|srcset|poster)=([\"'])(.*?)\1",
    re.IGNORECASE,
)
CSS_ASSET = re.compile(r"url\(\s*([\"']?)(.*?)\1\s*\)", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXPLICIT_ID = re.compile(r"\bid=[\"']([^\"']+)[\"']", re.IGNORECASE)
SKILL_REFERENCE = re.compile(
    r"\$(specsfy-[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(?![a-z0-9-])"
)
INTERNAL_ABSOLUTE = re.compile(
    r"https://(?:raw\.githubusercontent\.com/promovaweb/specsfy/main/"
    r"|github\.com/promovaweb/specsfy/(?:blob|tree)/main/)"
)
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


def authored_files(*suffixes: str) -> list[Path]:
    return sorted(
        path
        for suffix in suffixes
        for path in ROOT.rglob(f"*{suffix}")
        if not any(part in IGNORED_PARTS for part in path.relative_to(ROOT).parts)
    )


def github_anchor(title: str) -> str:
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"[^\w\- ]", "", title.casefold(), flags=re.UNICODE)
    return title.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return {
        *(github_anchor(title) for title in HEADING.findall(text)),
        *EXPLICIT_ID.findall(text),
    }


def markdown_targets(text: str) -> list[str]:
    targets = [*MARKDOWN_LINK.findall(text), *REFERENCE_LINK.findall(text)]
    for _quote, value in HTML_ASSET.findall(text):
        targets.extend(value.split() if " " not in value.strip() else [value])
    return targets


def local_destination(source: Path, raw_target: str) -> tuple[Path, str] | None:
    target = raw_target.strip().strip("<>")
    if (
        not target
        or "..." in target
        or target.startswith(("#", "/", "{", "$"))
    ):
        if target.startswith("#"):
            return source, urllib.parse.unquote(target[1:])
        return None
    parsed = urllib.parse.urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith("//"):
        return None
    destination = (source.parent / urllib.parse.unquote(parsed.path)).resolve()
    return destination, urllib.parse.unquote(parsed.fragment)


class RepositoryReferenceTests(unittest.TestCase):
    def test_all_authored_markdown_links_and_anchors_resolve(self) -> None:
        failures: list[str] = []
        for source in authored_files(".md"):
            text = source.read_text(encoding="utf-8")
            for raw_target in markdown_targets(text):
                resolved = local_destination(source, raw_target)
                if resolved is None:
                    continue
                destination, anchor = resolved
                label = source.relative_to(ROOT)
                if not destination.exists():
                    failures.append(f"{label} -> {raw_target}")
                    continue
                if anchor:
                    if not destination.is_file() or anchor not in anchors(destination):
                        failures.append(f"{label} -> {raw_target} (âncora)")
        self.assertEqual([], failures)

    def test_html_css_and_svg_assets_resolve(self) -> None:
        failures: list[str] = []
        for source in authored_files(".html", ".css", ".svg"):
            text = source.read_text(encoding="utf-8")
            targets = [value for _quote, value in HTML_ASSET.findall(text)]
            targets.extend(value for _quote, value in CSS_ASSET.findall(text))
            for raw_target in targets:
                if raw_target.startswith("data:"):
                    continue
                resolved = local_destination(source, raw_target)
                if resolved is None:
                    continue
                destination, _anchor = resolved
                if not destination.exists():
                    failures.append(
                        f"{source.relative_to(ROOT)} -> {raw_target}"
                    )
        self.assertEqual([], failures)

    def test_internal_navigation_and_images_do_not_use_remote_git_urls(self) -> None:
        failures = []
        for source in authored_files(".md", ".html"):
            if INTERNAL_ABSOLUTE.search(source.read_text(encoding="utf-8")):
                failures.append(str(source.relative_to(ROOT)))
        self.assertEqual([], failures)

    def test_repository_images_are_well_formed(self) -> None:
        failures: list[str] = []
        for path in authored_files(*IMAGE_SUFFIXES):
            relative = path.relative_to(ROOT)
            try:
                data = path.read_bytes()
                suffix = path.suffix.casefold()
                if suffix == ".png":
                    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
                        raise ValueError("assinatura PNG inválida")
                    width, height = struct.unpack(">II", data[16:24])
                    if width < 1 or height < 1:
                        raise ValueError("dimensões PNG inválidas")
                elif suffix == ".jpg" or suffix == ".jpeg":
                    if not (data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9")):
                        raise ValueError("assinatura JPEG inválida")
                elif suffix == ".gif":
                    if data[:6] not in {b"GIF87a", b"GIF89a"}:
                        raise ValueError("assinatura GIF inválida")
                elif suffix == ".webp":
                    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
                        raise ValueError("assinatura WebP inválida")
                elif suffix == ".svg":
                    root = ET.fromstring(data)
                    if not root.tag.endswith("svg"):
                        raise ValueError("raiz SVG inválida")
            except (OSError, ValueError, ET.ParseError) as error:
                failures.append(f"{relative}: {error}")
        self.assertEqual([], failures)

    def test_skill_references_and_specialist_catalog_are_coherent(self) -> None:
        skill_roots = (
            ROOT / ".agents/skills",
            ROOT / "skills",
            ROOT / "specialists",
        )
        available = {
            directory.name
            for root in skill_roots
            for directory in root.iterdir()
            if directory.is_dir() and (directory / "SKILL.md").is_file()
        }
        metadata_failures: list[str] = []
        for root in skill_roots:
            for directory in root.iterdir():
                skill = directory / "SKILL.md"
                if not directory.is_dir() or not skill.is_file():
                    continue
                skill_text = skill.read_text(encoding="utf-8")
                agent = directory / "agents/openai.yaml"
                if f"name: {directory.name}" not in skill_text:
                    metadata_failures.append(f"{directory.name}: frontmatter")
                if not agent.is_file() or f"${directory.name}" not in agent.read_text(
                    encoding="utf-8"
                ):
                    metadata_failures.append(f"{directory.name}: openai.yaml")
        self.assertEqual([], metadata_failures)

        unknown: set[str] = set()
        for source in authored_files(".md", ".yaml", ".yml"):
            text = source.read_text(encoding="utf-8")
            unknown.update(
                name for name in SKILL_REFERENCE.findall(text) if name not in available
            )
        self.assertEqual(set(), unknown)

        payload = json.loads(
            (ROOT / "specialists/catalog.json").read_text(encoding="utf-8")
        )
        names = {entry["name"] for entry in payload["skills"]}
        specialist_directories = {
            directory.name
            for directory in (ROOT / "specialists").iterdir()
            if directory.is_dir() and (directory / "SKILL.md").is_file()
        }
        self.assertEqual(specialist_directories, names)
        missing_requirements = {
            required
            for entry in payload["skills"]
            for required in entry.get("requires", [])
            if required not in names
        }
        self.assertEqual(set(), missing_requirements)


if __name__ == "__main__":
    unittest.main()
