from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
BUILDER = (
    ROOT
    / "specsfy-documentator"
    / "scripts"
    / "build_documentation.py"
)
EXPECTED = {
    "README.md",
    "architecture.md",
    "application.md",
    "database.md",
    "flows.md",
    "testing.md",
    "frontend.md",
    "packages.md",
    "integrations.md",
    "decisions.md",
}


def project(context) -> Path:
    temporary = tempfile.TemporaryDirectory()
    context.add_cleanup(temporary.cleanup)
    return Path(temporary.name)


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", "-B", str(BUILDER), "--project", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


@given("uma aplicação Laravel existente com banco, rotas, testes e frontend")
def given_laravel_application(context) -> None:
    context.project = project(context)
    write(
        context.project,
        "composer.json",
        '{"require":{"laravel/framework":"^12.0"},'
        '"require-dev":{"pestphp/pest":"^4.0"}}',
    )
    write(context.project, "package.json", '{"dependencies":{"react":"19.0.0","tailwindcss":"4.0.0"}}')
    write(context.project, "routes/web.php", "<?php Route::get('/orders', [OrderController::class, 'index']);")
    write(context.project, "app/Http/Controllers/OrderController.php", "<?php class OrderController {}")
    write(context.project, "app/Models/Order.php", "<?php class Order extends Model {}")
    write(context.project, "resources/views/orders.blade.php", "<div>Orders</div>")
    write(context.project, "resources/js/Orders.jsx", "export function Orders(){ return <main /> }")
    write(context.project, "resources/css/app.css", "@import 'tailwindcss';")
    write(
        context.project,
        "database/migrations/2026_create_orders.php",
        "<?php Schema::create('orders', function ($table) {$table->id();});",
    )
    write(context.project, "tests/Feature/OrdersTest.php", "<?php test('orders', fn () => true);")


@when("a skill specsfy-documentator constrói a documentação")
def when_documentator_builds(context) -> None:
    context.result = build(context.project)
    assert context.result.returncode == 0, context.result.stderr
    context.docs = {
        path.name: path.read_text(encoding="utf-8")
        for path in (context.project / "docs").glob("*.md")
    }


@then("docs contém arquitetura aplicação banco fluxos testes frontend pacotes integrações e decisões")
def then_docs_has_complete_topology(context) -> None:
    assert set(context.docs) == EXPECTED


@then("os mapas usam Mermaid para componentes fluxo classes e entidades")
def then_docs_has_mermaid_maps(context) -> None:
    joined = "\n".join(context.docs.values())
    for diagram in ("flowchart", "classDiagram", "erDiagram", "sequenceDiagram"):
        assert diagram in joined


@then("controllers models views React Tailwind e Pest são inventariados")
def then_laravel_elements_are_inventoried(context) -> None:
    joined = "\n".join(context.docs.values())
    for term in ("OrderController", "Order", "orders.blade.php", "React", "Tailwind", "Pest"):
        assert term in joined


@given("uma aplicação Node existente com Next React Tailwind e Vitest")
def given_node_application(context) -> None:
    context.project = project(context)
    write(
        context.project,
        "package.json",
        '{"scripts":{"test":"vitest run"},'
        '"dependencies":{"next":"15.0.0","react":"19.0.0","tailwindcss":"4.0.0"},'
        '"devDependencies":{"vitest":"3.0.0"}}',
    )
    write(context.project, "app/page.tsx", "export default function Page(){ return <Dashboard /> }")
    write(context.project, "app/api/orders/route.ts", "export async function GET() {}")
    write(context.project, "components/Dashboard.tsx", "export function Dashboard(){ return <main /> }")
    write(context.project, "tests/dashboard.test.tsx", "import { test } from 'vitest'; test('dashboard', () => {});")
    write(context.project, "tailwind.config.ts", "export default { theme: {} }")


@then("a documentação descreve páginas componentes APIs testes e comandos")
def then_node_docs_describe_application(context) -> None:
    joined = "\n".join(context.docs.values())
    for term in ("app/page.tsx", "Dashboard", "app/api/orders/route.ts", "Vitest", "vitest run"):
        assert term in joined


@then("cada pacote possui classificação versão fonte e referência GitHub")
def then_packages_have_provenance(context) -> None:
    packages = context.docs["packages.md"]
    for heading in ("Framework", "Integrado", "Terceiro", "GitHub"):
        assert heading in packages
    assert "https://github.com/" in packages


@given("uma documentação gerada com observações adicionadas pela equipe")
def given_generated_docs_with_human_notes(context) -> None:
    context.project = project(context)
    write(context.project, "package.json", '{"dependencies":{"react":"19.0.0"}}')
    write(context.project, "src/App.tsx", "export function App(){ return <main /> }")
    first = build(context.project)
    assert first.returncode == 0, first.stderr
    readme = context.project / "docs/README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nNota humana preservada.\n",
        encoding="utf-8",
    )


@when("o documentador é executado novamente depois de uma implementação")
def when_documentator_rebuilds(context) -> None:
    write(context.project, "src/OrderExporter.ts", "export class OrderExporter {}")
    context.result = build(context.project)
    assert context.result.returncode == 0, context.result.stderr


@then("os blocos detectados refletem o código atual")
def then_blocks_reflect_current_code(context) -> None:
    application = (context.project / "docs/application.md").read_text(encoding="utf-8")
    assert "OrderExporter" in application


@then("o conteúdo humano fora dos blocos permanece intacto")
def then_human_content_remains(context) -> None:
    readme = (context.project / "docs/README.md").read_text(encoding="utf-8")
    assert "Nota humana preservada." in readme
