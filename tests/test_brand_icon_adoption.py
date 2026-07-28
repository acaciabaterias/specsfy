from __future__ import annotations

import os
import struct
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
class BrandIconAdoptionTests(unittest.TestCase):
    def test_all_tracked_readmes_use_the_official_theme_aware_logo(
        self,
    ) -> None:
        tracked_files = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.split("\0")
        readmes = sorted(
            ROOT / relative_path
            for relative_path in tracked_files
            if Path(relative_path).name == "README.md"
        )
        self.assertTrue(readmes)

        for readme_path in readmes:
            with self.subTest(readme=readme_path.relative_to(ROOT)):
                logo_root = Path(
                    os.path.relpath(
                        ROOT / "brand" / "logo",
                        start=readme_path.parent,
                    )
                ).as_posix()
                readme = readme_path.read_text(encoding="utf-8")
                self.assertIn(
                    f'media="(prefers-color-scheme: dark)" '
                    f'srcset="{logo_root}/logo-dark.svg"',
                    readme,
                )
                self.assertIn(
                    f'media="(prefers-color-scheme: light)" '
                    f'srcset="{logo_root}/logo-light.svg"',
                    readme,
                )
                self.assertIn(
                    f'<img src="{logo_root}/logo-light.svg" '
                    'alt="Logo oficial do Specsfy" width="180">',
                    readme,
                )

    def test_brand_owns_accessible_vector_and_raster_sources(self) -> None:
        svg_path = ROOT / "brand" / "icons" / "icon.svg"
        png_path = ROOT / "brand" / "icons" / "icon.png"

        svg_root = ET.parse(svg_path).getroot()
        self.assertEqual("0 0 512 512", svg_root.attrib["viewBox"])
        self.assertEqual("img", svg_root.attrib["role"])
        title = next(child for child in svg_root if child.tag.endswith("title"))
        description = next(
            child for child in svg_root if child.tag.endswith("desc")
        )
        self.assertEqual("Ícone do framework Specsfy", title.text)
        self.assertIn("três placas empilhadas", description.text or "")

        png = png_path.read_bytes()
        self.assertEqual(b"\x89PNG\r\n\x1a\n", png[:8])
        width, height = struct.unpack(">II", png[16:24])
        self.assertEqual((512, 512), (width, height))

    def test_brand_sources_define_the_framework_icon_role_and_formats(self) -> None:
        for relative_path in (
            "README.md",
            "guidelines.md",
            "logo/logo.md",
            "icons/icons.md",
            "checklist.md",
            "guide/brand-guide.md",
            "style-guide.html",
        ):
            with self.subTest(source=relative_path):
                source = (ROOT / "brand" / relative_path).read_text(
                    encoding="utf-8"
                )
                self.assertIn("ícone do framework", source.lower())
                self.assertIn("icon.svg", source)
                self.assertIn("icon.png", source)

    def test_brand_guide_build_publishes_incremental_pdf_at_repository_root(
        self,
    ) -> None:
        brand_root = ROOT / "brand"
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        build_script = (ROOT / ".pdf" / "build-brand-guide.sh").read_text(
            encoding="utf-8"
        )
        pdf_style = (ROOT / ".pdf" / "style.css").read_text(encoding="utf-8")
        manual = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue((brand_root / "Specsfy-Manual-de-Marca.pdf").is_file())
        self.assertFalse(
            (brand_root / "guide" / "Specsfy-Manual-de-Marca.pdf").exists()
        )
        self.assertFalse((brand_root / "Makefile").exists())
        self.assertFalse((brand_root / "guide" / "build.sh").exists())
        self.assertIn(
            'OUT_PDF="$BRAND_ROOT/Specsfy-Manual-de-Marca.pdf"',
            build_script,
        )
        self.assertIn(".pdf/style.css", build_script)
        self.assertIn("brand-guide:", makefile)
        for dependency in (
            "brand/guide/brand-guide.md",
            "brand/guide/template.html",
            ".pdf/build-brand-guide.sh",
            ".pdf/style.css",
            "brand/style-guide.html",
        ):
            self.assertIn(dependency, makefile)
        self.assertIn("make brand-guide", manual)
        for evidence in (
            "@page",
            "--midnight-mirage: #001F3F",
            "--praxeti-white: #F6F7ED",
            "--mantis: #74C365",
            "IBM Plex Sans",
            "IBM Plex Mono",
        ):
            self.assertIn(evidence, pdf_style)


if __name__ == "__main__":
    unittest.main()
