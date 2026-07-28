import json
import re
import subprocess
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
EBOOK_ROOT = ROOT / "ebook"


@given("o percurso completo de documentação do usuário")
def given_user_documentation(context) -> None:
    context.user_pages = sorted((ROOT / "docs" / "user").rglob("*.md"))


@given("o arquivo de versão do ebook")
def given_ebook_version(context) -> None:
    context.version_path = EBOOK_ROOT / "VERSION"


@given("o manifesto verificável do ebook")
def given_ebook_manifest(context) -> None:
    context.manifest_path = EBOOK_ROOT / "build.json"


@given("as fontes visuais do ebook")
def given_ebook_visual_sources(context) -> None:
    context.visual_sources = (
        ROOT / ".ebook" / "pdf.css",
        ROOT / ".ebook" / "epub.css",
        ROOT / ".ebook" / "template.html",
    )


@given("a ordem canônica de leitura do usuário")
def given_canonical_reading_order(context) -> None:
    context.reading_order_path = (
        ROOT / "docs" / "user" / "reading-order.txt"
    )


@when("o contrato editorial do ebook é inspecionado")
def when_editorial_contract_is_inspected(context) -> None:
    context.version = (EBOOK_ROOT / "VERSION").read_text(
        encoding="utf-8"
    ).strip()
    context.manifest = json.loads(
        (EBOOK_ROOT / "build.json").read_text(encoding="utf-8")
    )
    context.order = [
        line
        for line in (ROOT / "docs" / "user" / "reading-order.txt").read_text(
            encoding="utf-8"
        ).splitlines()
        if line and not line.startswith("#")
    ]


@when("a integridade das fontes e dos artefatos é calculada")
def when_integrity_is_calculated(context) -> None:
    context.check = subprocess.run(
        [str(ROOT / ".ebook" / "build-ebook.sh"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    context.manifest = json.loads(
        context.manifest_path.read_text(encoding="utf-8")
    )


@when("o percurso pedagógico é inspecionado")
def when_pedagogical_path_is_inspected(context) -> None:
    context.reading_order = [
        line
        for line in context.reading_order_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line and not line.startswith("#")
    ]
    context.user_portal = (ROOT / "docs" / "user" / "README.md").read_text(
        encoding="utf-8"
    )
    context.build_script = (
        ROOT / ".ebook" / "build-ebook.sh"
    ).read_text(encoding="utf-8")


@then("PDF e EPUB versionados existem na pasta ebook")
def then_versioned_artifacts_exist(context) -> None:
    stem = f"Specsfy-Guia-do-Usuario-v{context.version}"
    assert (EBOOK_ROOT / f"{stem}.pdf").is_file()
    assert (EBOOK_ROOT / f"{stem}.epub").is_file()


@then("todas as páginas do usuário aparecem na ordem editorial")
def then_all_user_pages_are_ordered(context) -> None:
    expected = {
        path.relative_to(ROOT).as_posix() for path in context.user_pages
    }
    assert set(context.order) == expected
    assert len(context.order) == len(expected)


@then("a edição usa uma versão SemVer válida")
def then_version_is_semver(context) -> None:
    assert re.fullmatch(
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)",
        context.version,
    )


@then("os metadados dos artefatos usam a mesma versão")
def then_metadata_uses_version(context) -> None:
    assert context.manifest["version"] == context.version
    assert context.manifest["edition"] == f"v{context.version}"


@then("o digest cobre recursivamente os docs do usuário")
def then_digest_covers_user_docs(context) -> None:
    assert context.check.returncode == 0, context.check.stderr
    sources = set(context.manifest["sources"])
    expected = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs" / "user").rglob("*")
        if path.is_file()
    }
    assert expected <= sources
    assert re.fullmatch(r"[0-9a-f]{64}", context.manifest["source_sha256"])


@then("os hashes do PDF e EPUB correspondem ao manifesto")
def then_artifact_hashes_match(context) -> None:
    assert context.check.returncode == 0, context.check.stderr
    assert set(context.manifest["artifacts"]) == {"pdf", "epub"}
    for artifact in context.manifest["artifacts"].values():
        assert re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"])


@then("logo tipografia cores e templates derivam do manual da marca")
def then_visual_system_matches_brand(context) -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in context.visual_sources
    )
    for evidence in (
        "brand/logo/icon.svg",
        "IBM Plex Sans",
        "IBM Plex Mono",
        "#000000",
        "#FFFFFF",
    ):
        assert evidence in combined


@then(
    "metodologia instalação primeiro uso fluxo base operação e avançado "
    "aparecem nessa ordem"
)
def then_pedagogical_stages_are_ordered(context) -> None:
    milestones = (
        "docs/user/method.md",
        "docs/user/installation.md",
        "docs/user/getting-started.md",
        "docs/user/skills/README.md",
        "docs/user/cli.md",
        "docs/user/advanced-usage.md",
    )
    positions = [context.reading_order.index(item) for item in milestones]
    assert positions == sorted(positions)


@then("o portal e o ebook usam a mesma sequência")
def then_portal_and_ebook_share_sequence(context) -> None:
    assert "## Percurso pedagógico" in context.user_portal
    assert "docs/user/reading-order.txt" in context.build_script
    for relative in context.reading_order[1:]:
        link = relative.removeprefix("docs/user/")
        assert f"]({link})" in context.user_portal
