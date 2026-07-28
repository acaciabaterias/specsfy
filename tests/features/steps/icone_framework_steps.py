from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
REPOSITORIES = (
    ROOT,
    ROOT / "brand",
    ROOT / "skills",
    ROOT / "docs",
    ROOT / "example",
    ROOT / "specsfy",
    ROOT / "specialists",
    ROOT / "cli",
)
@given("os novos arquivos SVG e PNG do ícone do framework")
def given_framework_icon_files(context) -> None:
    context.svg = ROOT / "brand" / "icons" / "icon.svg"
    context.png = ROOT / "brand" / "icons" / "icon.png"


@when("a adoção visual do workspace é inspecionada")
def when_visual_adoption_is_inspected(context) -> None:
    context.readmes = {
        repository: (repository / "README.md").read_text(encoding="utf-8")
        for repository in REPOSITORIES
    }
    context.brand_sources = tuple(
        (ROOT / "brand" / path).read_text(encoding="utf-8")
        for path in (
            "README.md",
            "guidelines.md",
            "logo/logo.md",
            "icons/icons.md",
            "checklist.md",
            "guide/brand-guide.md",
            "style-guide.html",
        )
    )


@then("os dois formatos permanecem canônicos no repositório de marca")
def then_both_formats_are_canonical(context) -> None:
    assert context.svg.is_file()
    assert context.png.is_file()
    svg = context.svg.read_text(encoding="utf-8")
    assert 'viewBox="0 0 512 512"' in svg
    assert "Ícone do framework Specsfy" in svg
    assert "três placas empilhadas" in svg
    assert context.png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


@then("os oito READMEs exibem o SVG com fallback PNG")
def then_readmes_display_both_formats(context) -> None:
    for repository, readme in context.readmes.items():
        icon_root = (
            "brand/icons"
            if repository == ROOT
            else "icons"
            if repository == ROOT / "brand"
            else "../brand/icons"
        )
        assert f'{icon_root}/icon.svg' in readme
        assert f'{icon_root}/icon.png' in readme
        assert 'alt="Ícone do framework Specsfy"' in readme


@then("o manual distingue o ícone do framework do logo e dos ícones conceituais")
def then_manual_distinguishes_visual_assets(context) -> None:
    for source in context.brand_sources:
        assert "ícone do framework" in source.lower()
        assert "icon.svg" in source
        assert "icon.png" in source


@given("a fonte Markdown do guia completo de marca")
def given_complete_brand_guide_source(context) -> None:
    context.brand_root = ROOT / "brand"
    context.guide_source = context.brand_root / "guide" / "brand-guide.md"


@when("o contrato de build do manual é inspecionado")
def when_brand_guide_build_contract_is_inspected(context) -> None:
    context.makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    context.build_script = (ROOT / ".pdf" / "build-brand-guide.sh").read_text(
        encoding="utf-8"
    )
    context.pdf_style = (ROOT / ".pdf" / "style.css").read_text(encoding="utf-8")


@then("o PDF canônico fica na raiz do repositório de marca")
def then_canonical_pdf_is_at_brand_root(context) -> None:
    assert (context.brand_root / "Specsfy-Manual-de-Marca.pdf").is_file()
    assert not (
        context.brand_root / "guide" / "Specsfy-Manual-de-Marca.pdf"
    ).exists()


@then("o monorepo possui o gerador e a folha de estilo da marca")
def then_monorepo_owns_generator_and_brand_stylesheet(context) -> None:
    assert not (context.brand_root / "Makefile").exists()
    assert not (context.brand_root / "guide" / "build.sh").exists()
    assert 'OUT_PDF="$BRAND_ROOT/Specsfy-Manual-de-Marca.pdf"' in (
        context.build_script
    )
    assert ".pdf/style.css" in context.build_script
    for evidence in (
        "@page",
        "--midnight-mirage: #001F3F",
        "--praxeti-white: #F6F7ED",
        "--mantis: #74C365",
        "IBM Plex Sans",
        "IBM Plex Mono",
    ):
        assert evidence in context.pdf_style


@then("o comando make brand-guide reconstrói o PDF quando suas fontes mudam")
def then_make_command_rebuilds_pdf_from_sources(context) -> None:
    assert "brand-guide:" in context.makefile
    assert "brand/guide/brand-guide.md" in context.makefile
    assert ".pdf/build-brand-guide.sh" in context.makefile
    assert ".pdf/style.css" in context.makefile
    assert "make brand-guide" in (
        ROOT / "README.md"
    ).read_text(encoding="utf-8")
