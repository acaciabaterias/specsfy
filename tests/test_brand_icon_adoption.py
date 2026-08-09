from __future__ import annotations

import json
import os
import struct
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAND_ROOT = ROOT / "brand"
LOGO_ROOT = BRAND_ROOT / "logo"
REMOVED_LOGO_ASSETS = (
    "mark.svg",
    "favicon.svg",
    "logo/logo.md",
)


def tracked_readmes() -> list[Path]:
    tracked_files = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split("\0")
    return sorted(
        ROOT / relative_path
        for relative_path in tracked_files
        if Path(relative_path).name == "README.md"
    )


class BrandLogoAdoptionTests(unittest.TestCase):
    def test_all_tracked_readmes_use_the_canonical_logo_with_png_fallback(
        self,
    ) -> None:
        readmes = tracked_readmes()
        self.assertTrue(readmes)

        for readme_path in readmes:
            with self.subTest(readme=readme_path.relative_to(ROOT)):
                logo_root = Path(
                    os.path.relpath(LOGO_ROOT, start=readme_path.parent)
                ).as_posix()
                readme = readme_path.read_text(encoding="utf-8")
                self.assertIn(
                    f'<source srcset="{logo_root}/icon.svg" '
                    'type="image/svg+xml">',
                    readme,
                )
                self.assertIn(
                    f'<img src="{logo_root}/icon.png" '
                    'alt="Logo do Specsfy" width="128">',
                    readme,
                )
                for removed_asset in REMOVED_LOGO_ASSETS:
                    self.assertNotIn(removed_asset, readme)

    def test_brand_owns_the_layered_vector_and_raster_logo(self) -> None:
        svg_path = LOGO_ROOT / "icon.svg"
        png_path = LOGO_ROOT / "icon.png"

        svg_root = ET.parse(svg_path).getroot()
        self.assertEqual("512", svg_root.attrib["width"])
        self.assertEqual("512", svg_root.attrib["height"])
        self.assertEqual("0 0 512 512", svg_root.attrib["viewBox"])
        self.assertEqual("img", svg_root.attrib["role"])

        title = next(child for child in svg_root if child.tag.endswith("title"))
        description = next(
            child for child in svg_root if child.tag.endswith("desc")
        )
        self.assertEqual("Ícone principal do Specsfy", title.text)
        self.assertIn("Camadas de especificação e código", description.text or "")
        svg = svg_path.read_text(encoding="utf-8")
        for color in ("#00161E", "#A866FF", "#2AD5BE", "#C4B5FD"):
            self.assertIn(color, svg)

        png = png_path.read_bytes()
        self.assertEqual(b"\x89PNG\r\n\x1a\n", png[:8])
        width, height = struct.unpack(">II", png[16:24])
        self.assertEqual((512, 512), (width, height))

        self.assertFalse((BRAND_ROOT / "icons" / "icon.svg").exists())
        self.assertFalse((BRAND_ROOT / "icons" / "icon.png").exists())

    def test_logo_manual_and_brand_sources_describe_the_new_identity(self) -> None:
        logo_manual = (LOGO_ROOT / "LOGO.md").read_text(encoding="utf-8")
        for section in (
            "# Sistema de logo do Specsfy",
            "## Variantes",
            "## Proteção e tamanho",
            "## Restrições",
        ):
            self.assertIn(section, logo_manual)
        for evidence in (
            "512",
            "três camadas",
            "código",
            "`icon.svg`",
            "`icon.png`",
            "28 px",
            "12,5%",
            "petróleo",
            "violeta",
        ):
            self.assertIn(evidence, logo_manual)

        for relative_path in (
            "README.md",
            "guidelines.md",
            "checklist.md",
            "guide/brand-guide.md",
            "style-guide.html",
            "icons/icons.md",
        ):
            with self.subTest(source=relative_path):
                source = (BRAND_ROOT / relative_path).read_text(
                    encoding="utf-8"
                )
                self.assertIn("camadas", source.lower())
                self.assertTrue(
                    "icon.svg" in source or "logo-light.svg" in source or "brand/logo/" in source,
                    "a fonte deve apontar para uma variante canônica do logo",
                )
                for removed_asset in REMOVED_LOGO_ASSETS:
                    self.assertNotIn(removed_asset, source)

    def test_brand_color_sources_follow_the_monochrome_logo(self) -> None:
        palette = (BRAND_ROOT / "colors" / "palette.md").read_text(
            encoding="utf-8"
        )
        tokens_css = (BRAND_ROOT / "colors" / "tokens.css").read_text(
            encoding="utf-8"
        )
        tokens_json = json.loads(
            (BRAND_ROOT / "colors" / "tokens.json").read_text(
                encoding="utf-8"
            )
        )

        for evidence in (
            "#00161E",
            "#FFFFFF",
            "petróleo",
            "logo",
        ):
            self.assertIn(evidence, palette)
        self.assertIn("@import \"../global.css\"", tokens_css)
        self.assertEqual(
            "#00161E",
            tokens_json["families"]["primary"]["950"],
        )
        self.assertEqual(
            "#FFFFFF",
            tokens_json["light"]["background"],
        )
        for removed_color in (
            "Midnight Mirage",
            "Nuit Blanche",
            "Picture Book Green",
            "Mantis",
            "First Colors of Spring",
            "Praxeti White",
        ):
            self.assertNotIn(removed_color, palette)

    def test_brand_guide_build_tracks_the_new_logo_sources(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        build_script = (ROOT / ".pdf" / "build-brand-guide.sh").read_text(
            encoding="utf-8"
        )
        pdf_style = (ROOT / ".pdf" / "style.css").read_text(encoding="utf-8")
        manual = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertTrue(
            (BRAND_ROOT / "Specsfy-Manual-de-Marca.pdf").is_file()
        )
        self.assertFalse(
            (BRAND_ROOT / "guide" / "Specsfy-Manual-de-Marca.pdf").exists()
        )
        self.assertIn(
            'OUT_PDF="$BRAND_ROOT/Specsfy-Manual-de-Marca.pdf"',
            build_script,
        )
        for required_source in (
            "$BRAND_ROOT/logo/LOGO.md",
            "$BRAND_ROOT/logo/icon.svg",
            "$BRAND_ROOT/logo/icon.png",
        ):
            self.assertIn(required_source, build_script)
        for dependency in (
            "brand/logo/LOGO.md",
            "brand/logo/icon.svg",
            "brand/logo/icon.png",
            "brand/guide/brand-guide.md",
            "brand/guide/template.html",
            "brand/style-guide.html",
            ".pdf/build-brand-guide.sh",
            ".pdf/style.css",
        ):
            self.assertIn(dependency, makefile)
        self.assertIn("make brand-guide", manual)
        for evidence in (
            "@page",
            "--brand-black: #00161E",
            "--brand-white: #F2F8F9",
            "Manrope",
            "JetBrains Mono",
        ):
            self.assertIn(evidence, pdf_style)


if __name__ == "__main__":
    unittest.main()
