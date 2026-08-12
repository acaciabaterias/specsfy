import os
import struct
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
BRAND_ROOT = ROOT / "brand"
LOGO_ROOT = BRAND_ROOT / "logo"
REMOVED_ASSETS = (
    "logo-light.svg",
    "logo-dark.svg",
    "mark.svg",
    "favicon.svg",
    "logo/logo.md",
)


@given("os novos arquivos SVG e PNG do logo")
def given_new_logo_files(context) -> None:
    context.svg_path = LOGO_ROOT / "icon.svg"
    context.png_path = LOGO_ROOT / "icon.png"


@when("a construção vetorial é inspecionada")
def when_vector_construction_is_inspected(context) -> None:
    context.svg_root = ET.parse(context.svg_path).getroot()
    context.png = context.png_path.read_bytes()


@then("o logo preserva as três camadas e o símbolo de código")
def then_logo_preserves_layers_and_code(context) -> None:
    assert context.svg_root.attrib["viewBox"] == "0 0 512 512"
    layer_ids = {
        child.attrib.get("id")
        for child in context.svg_root
        if child.tag.endswith("g")
    }
    assert layer_ids == {
        "layer-bottom",
        "layer-middle",
        "layer-top",
        "layer-code-left",
        "layer-code-slash",
        "layer-code-right",
    }


@then("o PNG preserva a prancheta quadrada de 512 pixels")
def then_png_preserves_square_canvas(context) -> None:
    assert context.png.startswith(b"\x89PNG\r\n\x1a\n")
    assert struct.unpack(">II", context.png[16:24]) == (512, 512)


@given("o manual normativo LOGO.md")
def given_normative_logo_manual(context) -> None:
    context.logo_manual_path = LOGO_ROOT / "LOGO.md"


@when("o contrato de identidade visual é inspecionado")
def when_visual_identity_contract_is_inspected(context) -> None:
    context.logo_manual = context.logo_manual_path.read_text(encoding="utf-8")
    context.brand_sources = tuple(
        (BRAND_ROOT / relative_path).read_text(encoding="utf-8")
        for relative_path in (
            "README.md",
            "guidelines.md",
            "checklist.md",
            "guide/brand-guide.md",
            "style-guide.html",
            "icons/icons.md",
        )
    )


@then(
    "construção cores proteção redução fundos e acessibilidade estão definidos"
)
def then_complete_logo_rules_are_defined(context) -> None:
    for section in (
        "## Construção",
        "## Cores",
        "## Área de proteção",
        "## Tamanho mínimo",
        "## Fundos",
        "## Acessibilidade",
        "## Usos incorretos",
    ):
        assert section in context.logo_manual


@then("os guias de marca não descrevem os ativos removidos")
def then_brand_guides_do_not_describe_removed_assets(context) -> None:
    for source in context.brand_sources:
        assert "três camadas" in source.lower()
        assert "símbolo de código" in source.lower()
        for removed_asset in REMOVED_ASSETS:
            assert removed_asset not in source


@given("os READMEs versionados encontrados recursivamente")
def given_tracked_readmes_recursively(context) -> None:
    tracked_files = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split("\0")
    context.readmes = sorted(
        ROOT / relative_path
        for relative_path in tracked_files
        if Path(relative_path).name == "README.md"
    )


@when("a adoção do novo logo nesses arquivos é inspecionada")
def when_new_logo_adoption_is_inspected(context) -> None:
    context.readme_contents = {
        path: path.read_text(encoding="utf-8")
        for path in context.readmes
    }


@then("todos os READMEs usam o SVG canônico com fallback PNG")
def then_all_readmes_use_canonical_logo(context) -> None:
    assert context.readme_contents
    for path, content in context.readme_contents.items():
        if path == ROOT / "cli" / "README.md":
            assert (
                'srcset="https://promovaweb.com/opensource/specsfy/icon.svg"'
                in content
            )
            assert (
                'src="https://promovaweb.com/opensource/specsfy/icon.png"'
                in content
            )
            continue
        logo_root = Path(
            os.path.relpath(LOGO_ROOT, start=path.parent)
        ).as_posix()
        assert (
            f'<source srcset="{logo_root}/icon.svg" '
            'type="image/svg+xml">'
        ) in content
        assert (
            f'<img src="{logo_root}/icon.png" '
            'alt="Logo do Specsfy" width="128">'
        ) in content


@given("a fonte Markdown do guia completo de marca")
def given_complete_brand_guide_source(context) -> None:
    context.guide_source = BRAND_ROOT / "guide" / "brand-guide.md"


@when("o contrato de build do manual é inspecionado")
def when_brand_guide_build_contract_is_inspected(context) -> None:
    context.makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    context.build_script = (ROOT / ".pdf" / "build-brand-guide.sh").read_text(
        encoding="utf-8"
    )


@then("o PDF canônico fica na raiz do repositório de marca")
def then_canonical_pdf_is_at_brand_root(context) -> None:
    assert (BRAND_ROOT / "Specsfy-Manual-de-Marca.pdf").is_file()
    assert not (
        BRAND_ROOT / "guide" / "Specsfy-Manual-de-Marca.pdf"
    ).exists()


@then("o build rastreia LOGO.md SVG PNG HTML Markdown e CSS")
def then_build_tracks_all_brand_sources(context) -> None:
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
        assert dependency in context.makefile
    for required_source in (
        "$BRAND_ROOT/logo/LOGO.md",
        "$BRAND_ROOT/logo/icon.svg",
        "$BRAND_ROOT/logo/icon.png",
    ):
        assert required_source in context.build_script
