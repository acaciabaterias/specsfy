from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "specsfy-documentator"
BUILDER = SKILL / "scripts" / "build_documentation.py"
EXPECTED_DOCS = {
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


def run_builder(project: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python3",
            "-B",
            str(BUILDER),
            "--project",
            str(project),
            *arguments,
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class DocumentatorTests(unittest.TestCase):
    def test_builds_rich_laravel_react_documentation_and_preserves_notes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            write(
                project / "composer.json",
                json.dumps(
                    {
                        "require": {
                            "php": "^8.4",
                            "laravel/framework": "^12.0",
                        },
                        "require-dev": {"pestphp/pest": "^4.0"},
                        "scripts": {"test": "php artisan test"},
                    }
                ),
            )
            write(
                project / "composer.lock",
                json.dumps(
                    {
                        "packages": [
                            {
                                "name": "laravel/framework",
                                "version": "v12.0.0",
                                "source": {
                                    "url": "https://github.com/laravel/framework.git"
                                },
                            }
                        ],
                        "packages-dev": [
                            {
                                "name": "pestphp/pest",
                                "version": "v4.0.0",
                                "source": {
                                    "url": "https://github.com/pestphp/pest.git"
                                },
                            }
                        ],
                    }
                ),
            )
            write(
                project / "package.json",
                json.dumps(
                    {
                        "dependencies": {
                            "react": "^19.0",
                            "tailwindcss": "^4.0",
                        },
                        "devDependencies": {"vite": "^7.0"},
                        "scripts": {"build": "vite build"},
                    }
                ),
            )
            write(
                project / "routes/web.php",
                "Route::get('/orders', [OrderController::class, 'index']);\n",
            )
            write(
                project / "app/Http/Controllers/OrderController.php",
                "<?php class OrderController { public function index() {} }\n",
            )
            write(
                project / "app/Models/Order.php",
                "<?php class Order extends Model { protected $fillable = ['total']; }\n",
            )
            write(project / "resources/views/orders/index.blade.php", "<h1>Orders</h1>\n")
            write(
                project / "resources/js/Components/OrderTable.tsx",
                "export function OrderTable(){ return <div className=\"grid gap-4\"/> }\n",
            )
            write(
                project / "resources/css/app.css",
                '@import "tailwindcss";\n@theme { --color-brand: #123456; }\n',
            )
            write(
                project / "database/migrations/2026_create_orders_table.php",
                "<?php Schema::create('orders', function (Blueprint $table) {"
                "$table->id(); $table->foreignId('user_id');"
                "$table->decimal('total'); });\n",
            )
            write(
                project / "tests/Feature/OrdersTest.php",
                "<?php test('lists orders', function () {});\n",
            )
            write(
                project / ".env.example",
                "DB_CONNECTION=pgsql\nSTRIPE_KEY=\n",
            )

            result = run_builder(project)

            self.assertEqual(0, result.returncode, result.stderr)
            docs = project / "docs"
            self.assertEqual(
                EXPECTED_DOCS,
                {path.name for path in docs.glob("*.md")},
            )
            combined = "\n".join(
                path.read_text(encoding="utf-8") for path in docs.glob("*.md")
            )
            for diagram in ("flowchart", "classDiagram", "erDiagram", "sequenceDiagram"):
                self.assertIn(diagram, combined)
            for term in (
                "OrderController",
                "Order",
                "orders/index.blade.php",
                "OrderTable",
                "Tailwind",
                "--color-brand",
                "Pest",
                "tests/Feature/OrdersTest.php",
                "laravel/framework",
                "https://github.com/laravel/framework",
            ):
                self.assertIn(term, combined)

            application = docs / "application.md"
            application.write_text(
                application.read_text(encoding="utf-8")
                + "\n## Nota humana\n\nPreservar esta explicação.\n",
                encoding="utf-8",
            )
            write(
                project / "app/Services/OrderExporter.php",
                "<?php class OrderExporter {}\n",
            )
            rebuilt = run_builder(project)
            self.assertEqual(0, rebuilt.returncode, rebuilt.stderr)
            application_content = application.read_text(encoding="utf-8")
            self.assertIn("OrderExporter", application_content)
            self.assertIn("Preservar esta explicação.", application_content)
            self.assertEqual(0, run_builder(project, "--check").returncode)

    def test_builds_node_next_react_testing_and_package_maps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            write(
                project / "package.json",
                json.dumps(
                    {
                        "dependencies": {
                            "next": "^16.0",
                            "react": "^19.0",
                            "tailwindcss": "^4.0",
                            "acme-sdk": "^2.0",
                        },
                        "devDependencies": {"vitest": "^4.0"},
                        "scripts": {
                            "test": "vitest run",
                            "build": "next build",
                        },
                    }
                ),
            )
            write(
                project / "node_modules/acme-sdk/package.json",
                json.dumps(
                    {
                        "name": "acme-sdk",
                        "repository": {
                            "type": "git",
                            "url": "git+https://github.com/acme/sdk.git",
                        },
                    }
                ),
            )
            write(
                project / "app/page.tsx",
                "export default function Page(){ return <Dashboard/> }\n",
            )
            write(
                project / "app/api/orders/route.ts",
                "export async function GET(){ return Response.json([]) }\n",
            )
            write(
                project / "components/Dashboard.tsx",
                "export function Dashboard(){ return <main className=\"mx-auto\"/> }\n",
            )
            write(
                project / "tests/dashboard.test.tsx",
                "import { test } from 'vitest'; test('dashboard', () => {});\n",
            )
            write(project / "tailwind.config.ts", "export default { theme: {} };\n")

            result = run_builder(project)

            self.assertEqual(0, result.returncode, result.stderr)
            combined = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (project / "docs").glob("*.md")
            )
            for term in (
                "Next.js",
                "app/page.tsx",
                "app/api/orders/route.ts",
                "Dashboard",
                "Vitest",
                "vitest run",
                "tailwind.config.ts",
                "https://github.com/acme/sdk",
            ):
                self.assertIn(term, combined)
            packages = (project / "docs/packages.md").read_text(encoding="utf-8")
            for heading in ("Categoria", "Escopo", "Versão", "Fonte", "GitHub"):
                self.assertIn(heading, packages)
            self.assertIn("| Terceiro | desenvolvimento | vitest |", packages)

    def test_skill_is_independent_and_mandatory_after_implementation(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        implementation = (
            ROOT / "specsfy-base-implement" / "SKILL.md"
        ).read_text(encoding="utf-8")
        framework = (ROOT / "Spec.md").read_text(encoding="utf-8")
        self.assertIn("código existente", skill)
        self.assertIn("build_documentation.py", skill)
        self.assertIn("$specsfy-documentator", implementation)
        self.assertIn("$specsfy-documentator", framework)


if __name__ == "__main__":
    unittest.main()
