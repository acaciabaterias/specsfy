from __future__ import annotations

import json
import re
import struct
import subprocess
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EBOOK_ROOT = ROOT / "ebook"
PIPELINE_ROOT = ROOT / ".ebook"


class UserEbookTests(unittest.TestCase):
    def test_semver_controls_versioned_pdf_and_epub(self) -> None:
        version = (EBOOK_ROOT / "VERSION").read_text(
            encoding="utf-8"
        ).strip()
        self.assertRegex(
            version,
            r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$",
        )
        stem = f"Specsfy-Guia-do-Usuario-v{version}"
        self.assertTrue((EBOOK_ROOT / f"{stem}.pdf").is_file())
        self.assertTrue((EBOOK_ROOT / f"{stem}.epub").is_file())

    def test_editorial_order_includes_every_user_page_once(self) -> None:
        ordered_sources = [
            line
            for line in (ROOT / "docs" / "user" / "reading-order.txt").read_text(
                encoding="utf-8"
            ).splitlines()
            if line and not line.startswith("#")
        ]
        user_pages = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "docs" / "user").rglob("*.md")
        }
        self.assertEqual(user_pages, set(ordered_sources))
        self.assertEqual(len(user_pages), len(ordered_sources))

    def test_build_manifest_proves_sources_and_artifacts_are_current(
        self,
    ) -> None:
        check = subprocess.run(
            [str(PIPELINE_ROOT / "build-ebook.sh"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, check.returncode, check.stderr)

        manifest = json.loads(
            (EBOOK_ROOT / "build.json").read_text(encoding="utf-8")
        )
        self.assertRegex(manifest["source_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual({"pdf", "epub"}, set(manifest["artifacts"]))
        for artifact in manifest["artifacts"].values():
            self.assertRegex(artifact["sha256"], r"^[0-9a-f]{64}$")

    def test_makefile_tracks_recursive_docs_and_exposes_ebook_target(
        self,
    ) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        for evidence in (
            ".PHONY: brand-guide ebook verify-ebook",
            "EBOOK_DOC_SOURCES",
            "find docs/user -type f",
            "ebook:",
            "./.ebook/build-ebook.sh",
            "verify-ebook:",
            "./.ebook/build-ebook.sh --check",
        ):
            self.assertIn(evidence, makefile)

    def test_visual_sources_reuse_the_brand_system(self) -> None:
        sources = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                PIPELINE_ROOT / "pdf.css",
                PIPELINE_ROOT / "epub.css",
                PIPELINE_ROOT / "template.html",
                PIPELINE_ROOT / "metadata.yaml",
            )
        )
        for evidence in (
            "brand/logo/icon.svg",
            "IBM Plex Sans",
            "IBM Plex Mono",
            "#000000",
            "#FFFFFF",
            "Specify. Prove. Ship.",
        ):
            self.assertIn(evidence, sources)

    def test_epub_is_well_formed_and_contains_navigation(self) -> None:
        version = (EBOOK_ROOT / "VERSION").read_text(
            encoding="utf-8"
        ).strip()
        epub = EBOOK_ROOT / f"Specsfy-Guia-do-Usuario-v{version}.epub"
        with zipfile.ZipFile(epub) as archive:
            self.assertEqual(
                b"application/epub+zip",
                archive.read("mimetype"),
            )
            names = set(archive.namelist())
            self.assertIn("META-INF/container.xml", names)
            self.assertTrue(
                any(name.endswith("nav.xhtml") for name in names)
            )
            for name in names:
                if name.endswith((".xhtml", ".opf", ".ncx", ".xml")):
                    with self.subTest(epub_entry=name):
                        ET.fromstring(archive.read(name))
            package = ET.fromstring(archive.read("EPUB/content.opf"))
            namespace = {"opf": "http://www.idpf.org/2007/opf"}
            cover = next(
                item
                for item in package.findall(".//opf:item", namespace)
                if "cover-image" in item.attrib.get("properties", "")
            )
            cover_data = archive.read(f"EPUB/{cover.attrib['href']}")
            self.assertEqual(b"\x89PNG\r\n\x1a\n", cover_data[:8])
            self.assertEqual(
                (1600, 2560),
                struct.unpack(">II", cover_data[16:24]),
            )
            title = package.find(
                ".//{http://purl.org/dc/elements/1.1/}title"
            )
            self.assertIsNotNone(title)
            self.assertIn(f"v{version}", title.text or "")


if __name__ == "__main__":
    unittest.main()
