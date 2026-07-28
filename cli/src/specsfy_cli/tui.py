from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.css.query import NoMatches
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Markdown,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from . import __version__
from .backlog import BacklogItem, backlogs_fingerprint, scan_backlogs
from .catalog import Catalog, CatalogEntry
from .config import load_config
from .installer import (
    AUXILIARY_SKILLS,
    BASE_SKILLS,
    DOCUMENTATION_SKILLS,
    FRAMEWORK_SKILLS,
    SkillInstaller,
)
from .progress import SpecProgress, scan_specs, specs_fingerprint, summarize_specs
from .skill_lock import (
    ensure_skills_lock,
    installed_skill_names,
    skills_lock_fingerprint,
)
from .testing import TestRun, stream_project_tests


BASE_DESCRIPTIONS = {
    "specsfy-base-backlog": "Ideias, descoberta inicial e backlog priorizado.",
    "specsfy-base-interview": "Entrevista arquitetural para reduzir ambiguidades.",
    "specsfy-base-specify": "Criação e evolução da especificação normativa.",
    "specsfy-base-validate": "Revisão de qualidade, riscos e gates.",
    "specsfy-base-tasks": "Decomposição rastreável do trabalho.",
    "specsfy-base-tdd-bdd": "BDD, TDD e rastreabilidade dos requisitos.",
    "specsfy-base-implement": "Execução disciplinada e evidências da entrega.",
    "specsfy-base-update-spec": "Atualiza pedidos tardios e reabre os gates afetados.",
    "specsfy-base-progress": "Leitura e acompanhamento do progresso.",
    "specsfy-setup": "Prepara e reconcilia o contexto persistente do projeto.",
    "specsfy-aux-stack": "Mapeia e mantém o stack técnico observado.",
    "specsfy-aux-rules": "Ajuda a registrar regras explícitas sem apagar as atuais.",
    "specsfy-aux-database": "Mantém o mapa tabular completo da persistência.",
    "specsfy-documentator": "Reconstrói a documentação técnica completa do sistema.",
}

CATEGORY_LABELS = {
    "base": "Essenciais",
    "auxiliary": "Auxiliares",
    "documentation": "Documentação",
    "architecture": "Arquitetura",
    "backend": "Backend",
    "data": "Dados",
    "design": "Design e experiência",
    "engineering": "Engenharia",
    "frontend": "Frontend",
    "language": "Linguagens",
    "operations": "Operações",
    "platform": "Plataforma",
    "quality": "Qualidade",
    "instalada": "Outras instaladas",
}


@dataclass(frozen=True)
class SkillOption:
    name: str
    description: str
    kind: str
    installed: bool


class SpecPreviewModal(ModalScreen[None]):
    BINDINGS = [
        Binding("escape", "close", "Voltar", priority=True),
    ]
    CSS = """
    SpecPreviewModal {
        align: center middle;
        background: #080b10 80%;
    }
    #spec-preview-dialog {
        width: 92%;
        height: 92%;
        padding: 1 2;
        background: #111820;
        border: round #58a6ff;
    }
    #spec-preview-title {
        height: auto;
        color: #f0f6fc;
        text-style: bold;
    }
    #spec-preview-metadata {
        height: auto;
        margin-bottom: 1;
        color: #9da9b7;
    }
    #spec-preview-scroll {
        height: 1fr;
        padding: 0 1;
        background: #0f141b;
        border: round #303b4d;
    }
    #spec-preview {
        height: auto;
        color: #d7e0ea;
    }
    #spec-preview-help {
        height: 1;
        margin-top: 1;
        color: #b7c3d0;
        content-align: center middle;
    }
    """

    def __init__(self, spec: SpecProgress) -> None:
        super().__init__()
        self.spec = spec

    def compose(self) -> ComposeResult:
        spec = self.spec
        with Vertical(id="spec-preview-dialog"):
            yield Static(
                f"{spec.slug} · {spec.status}",
                id="spec-preview-title",
                markup=False,
            )
            yield Static(
                f"{spec.title} · Gates {spec.passed_gates}/{spec.total_gates} · "
                f"Tarefas {spec.completed_tasks}/{spec.total_tasks} · "
                f"Checklist {spec.completed_items}/{spec.total_items} · "
                f"{spec.percent}%\n{spec.path}",
                id="spec-preview-metadata",
                markup=False,
            )
            with VerticalScroll(id="spec-preview-scroll", can_focus=True):
                yield Markdown(spec.content, id="spec-preview", open_links=False)
            yield Static(
                "↑/↓: rolar · Esc: voltar para a lista de specs",
                id="spec-preview-help",
            )

    def on_mount(self) -> None:
        self.query_one("#spec-preview-scroll", VerticalScroll).focus()

    def action_close(self) -> None:
        self.dismiss()


class SpecsfyApp(App):
    TITLE = "Specsfy"
    SUB_TITLE = "Dashboard de specs e skills"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("ctrl+q", "quit", "Sair", priority=True),
        Binding("escape", "back", "Voltar", priority=True),
        Binding("ctrl+u", "refresh", "Atualizar", priority=True, show=False),
        Binding("ctrl+b", "install_base", "Framework", priority=True, show=False),
        Binding("ctrl+d", "detect_skills", "Detectar", priority=True, show=False),
        Binding("ctrl+e", "toggle_skill", "Alternar", priority=True, show=False),
        Binding("space", "activate_selection", "Abrir/alternar", show=False),
        Binding("ctrl+a", "apply_skills", "Aplicar", priority=True, show=False),
        Binding(
            "ctrl+r",
            "update_skills",
            "Atualizar skills",
            priority=True,
            show=False,
        ),
        Binding("ctrl+m", "select_visible", "Marcar", priority=True, show=False),
        Binding("ctrl+l", "clear_visible", "Limpar", priority=True, show=False),
        Binding("ctrl+t", "filter_all", "Todas", priority=True, show=False),
        Binding(
            "ctrl+i",
            "filter_installed",
            "Instaladas",
            priority=True,
            show=False,
        ),
        Binding(
            "ctrl+c",
            "filter_detected",
            "Recomendadas",
            priority=True,
            show=False,
        ),
        Binding("ctrl+h", "show_home", "Home", priority=True, show=False),
        Binding(
            "ctrl+g",
            "show_backlogs",
            "Backlogs",
            priority=True,
            show=False,
        ),
        Binding("ctrl+s", "show_specs", "Specs", priority=True, show=False),
        Binding("ctrl+j", "show_tests", "Testes", priority=True, show=False),
        Binding(
            "ctrl+x",
            "run_tests",
            "Executar testes",
            priority=True,
            show=False,
        ),
        Binding("ctrl+k", "show_skills", "Skills", priority=True, show=False),
        Binding("ctrl+o", "show_about", "Sobre", priority=True, show=False),
    ]
    CSS = """
    Screen {
        layout: vertical;
        background: #0f141b;
        color: #e6edf3;
    }
    Header, Footer {
        background: #161d27;
        color: #f0f6fc;
    }
    .toolbar { height: auto; padding: 1; }
    #project {
        width: 1fr;
        background: #161d27;
        color: #f0f6fc;
        border: tall #303b4d;
    }
    #project:focus { border: tall #58a6ff; }
    #workspace-tabs { height: 1fr; }
    TabbedContent, TabPane { background: #0f141b; }
    #summary { height: 7; margin: 1; }
    .summary-card {
        width: 1fr;
        height: 6;
        margin-right: 1;
        padding: 1;
        color: #f0f6fc;
        content-align: center middle;
    }
    #summary-specs {
        background: #173e67;
        border: round #2f81f7;
    }
    #summary-tasks {
        background: #3f2d63;
        border: round #a371f7;
    }
    #summary-items {
        background: #174b43;
        border: round #2ea043;
    }
    #summary-progress {
        margin-right: 0;
        background: #4a381c;
        border: round #d29922;
    }
    #home-copy, #about-copy {
        margin: 1;
        padding: 1 2;
        background: #161d27;
        color: #d7e0ea;
        border: round #303b4d;
    }
    #status, #skills-status {
        height: auto;
        padding: 1;
        color: #9da9b7;
    }
    #skills-status {
        height: 1;
        padding: 0 1;
    }
    DataTable {
        background: #111820;
        color: #e6edf3;
    }
    DataTable > .datatable--header {
        background: #253044;
        color: #ffffff;
        text-style: bold;
    }
    DataTable > .datatable--cursor {
        background: #1f6feb;
        color: #ffffff;
        text-style: bold;
    }
    DataTable > .datatable--even-row { background: #161d27; }
    DataTable > .datatable--odd-row { background: #111820; }
    #progress { height: 1fr; margin: 1; border: round #303b4d; }
    #backlog-panel { height: 1fr; margin: 1; }
    #backlog-list-pane {
        width: 2fr;
        margin-right: 1;
        background: #111820;
        border: round #303b4d;
    }
    #backlog-list-title, #backlog-preview-title {
        height: auto;
        padding: 1;
        text-style: bold;
    }
    #backlog-list { height: 1fr; }
    #backlog-preview-pane {
        width: 4fr;
        padding: 0 2 1 2;
        background: #111820;
        border: round #303b4d;
    }
    #backlog-preview {
        height: auto;
        color: #d7e0ea;
    }
    MarkdownHeader, MarkdownH1, MarkdownH2, MarkdownH3 {
        color: #79c0ff;
        background: #111820;
        text-style: bold;
    }
    MarkdownParagraph { color: #d7e0ea; }
    #tests-toolbar {
        height: 4;
        padding: 1;
    }
    #tests-status {
        width: 1fr;
        height: 3;
        padding: 1;
        color: #b7c3d0;
    }
    #run-tests {
        width: 24;
        margin: 0 0 0 1;
    }
    #test-results-tabs {
        height: 1fr;
        margin: 0 1 1 1;
    }
    #tests-summary {
        height: 1fr;
        margin: 1;
        padding: 2;
        background: #161d27;
        color: #d7e0ea;
        border: round #303b4d;
    }
    #tests-output {
        height: 1fr;
        margin: 1;
        padding: 1;
        background: #080c12;
        color: #d7e0ea;
        border: round #303b4d;
    }
    #skills-catalog {
        height: 1fr;
        margin: 0 1;
    }
    #skills-table-pane {
        width: 2fr;
        margin-right: 1;
        background: #111820;
        border: round #303b4d;
    }
    #skills-table { height: 1fr; }
    #skill-detail-pane {
        width: 1fr;
        padding: 1;
        background: #161d27;
        border: round #303b4d;
    }
    #skill-detail {
        height: auto;
        color: #d7e0ea;
    }
    #skills-search-row {
        height: 3;
        padding: 0 1;
    }
    #skills-filters {
        grid-size: 3;
        grid-columns: 1fr 1fr 1fr;
        grid-rows: 3;
        grid-gutter: 0 1;
        height: 3;
        padding: 0 1;
    }
    #skills-actions {
        grid-size: 6;
        grid-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
        grid-rows: 3;
        grid-gutter: 0 1;
        height: 3;
        padding: 0 1;
    }
    #skills-search { width: 1fr; }
    #skills-selection-summary {
        height: 1;
        margin: 0 1;
        padding: 0 1;
        color: #9da9b7;
    }
    Button {
        margin-left: 1;
        background: #212b38;
        color: #e6edf3;
        border: tall #39475a;
    }
    Button:hover, Button:focus {
        background: #303d50;
        color: #ffffff;
        border: tall #58a6ff;
    }
    Button.-primary {
        background: #1f6feb;
        color: #ffffff;
        border: tall #58a6ff;
    }
    #skills-filters Button, #skills-actions Button {
        width: 1fr;
        margin: 0;
    }
    #keyboard-help {
        height: 1;
        padding: 0 1;
        background: #161d27;
        color: #b7c3d0;
    }
    """

    def __init__(
        self,
        project: Path | None = None,
        *,
        catalog: Catalog | None = None,
    ) -> None:
        super().__init__()
        self.project = (project or Path.cwd()).expanduser().resolve()
        self._fingerprint = ""
        self._backlog_fingerprint = ""
        self._backlogs: dict[str, BacklogItem] = {}
        self._selected_backlog_slug = ""
        self._specs: dict[str, SpecProgress] = {}
        self._selected_spec_slug = ""
        self._lock_fingerprint = ""
        self._catalog = catalog
        self._catalog_error = ""
        self._installed_skills: set[str] = set()
        self._selected_skills: set[str] = set()
        self._detected_skills: set[str] = set()
        self._skill_options_cache: list[SkillOption] = []
        self._selected_skill_name = ""
        self._skill_filter = "all"
        self._skills_initialized = False
        self._test_worker = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Horizontal(classes="toolbar"):
                yield Input(value=str(self.project), id="project")
                yield Button("Atualizar  ^U", id="refresh", variant="primary")
            with TabbedContent(id="workspace-tabs"):
                with TabPane("Home", id="tab-home"):
                    with Horizontal(id="summary"):
                        yield Static(id="summary-specs", classes="summary-card")
                        yield Static(id="summary-tasks", classes="summary-card")
                        yield Static(id="summary-items", classes="summary-card")
                        yield Static(id="summary-progress", classes="summary-card")
                    yield Static(
                        "Visão consolidada do andamento das especificações. "
                        "Os números são recalculados quando os arquivos mudam.",
                        id="home-copy",
                    )
                with TabPane("Backlogs", id="tab-backlogs"):
                    with Horizontal(id="backlog-panel"):
                        with Vertical(id="backlog-list-pane"):
                            yield Static("Backlogs", id="backlog-list-title")
                            yield DataTable(id="backlog-list")
                        with VerticalScroll(
                            id="backlog-preview-pane",
                            can_focus=True,
                        ):
                            yield Static(
                                "Selecione um backlog",
                                id="backlog-preview-title",
                            )
                            yield Markdown(
                                "Nenhum backlog selecionado.",
                                id="backlog-preview",
                                open_links=False,
                            )
                with TabPane("Specs", id="tab-specs"):
                    yield DataTable(id="progress")
                with TabPane("Testes", id="tab-tests"):
                    with Horizontal(id="tests-toolbar"):
                        yield Static(
                            "Nenhuma execução nesta sessão.",
                            id="tests-status",
                            markup=False,
                        )
                        yield Button(
                            "Executar testes  ^X",
                            id="run-tests",
                            variant="primary",
                        )
                    with TabbedContent(id="test-results-tabs"):
                        with TabPane("Resumo", id="tab-tests-summary"):
                            yield Static(id="tests-summary", markup=False)
                        with TabPane("Testes", id="tab-tests-output"):
                            yield RichLog(
                                id="tests-output",
                                wrap=True,
                                markup=False,
                                auto_scroll=True,
                            )
                with TabPane("Skills", id="tab-skills"):
                    yield Static("Carregando skills…", id="skills-status")
                    with Horizontal(id="skills-search-row"):
                        yield Input(
                            placeholder="Buscar por nome, tecnologia ou categoria…",
                            id="skills-search",
                        )
                        yield Button("Atualizar  ^R", id="update-skills")
                    with Grid(id="skills-filters"):
                        yield Button(
                            "Todas  ^T",
                            id="filter-all",
                            variant="primary",
                        )
                        yield Button("Instaladas  ^I", id="filter-installed")
                        yield Button("Recomendadas  ^C", id="filter-detected")
                    yield Static(id="skills-selection-summary")
                    with Horizontal(id="skills-catalog"):
                        with Vertical(id="skills-table-pane"):
                            yield DataTable(id="skills-table")
                        with VerticalScroll(
                            id="skill-detail-pane",
                            can_focus=True,
                        ):
                            yield Static(
                                "Selecione uma skill para ver os detalhes.",
                                id="skill-detail",
                                markup=False,
                            )
                    with Grid(id="skills-actions"):
                        yield Button("Detectar  ^D", id="detect")
                        yield Button("Framework  ^B", id="install")
                        yield Button("Marcar  ^M", id="select-visible")
                        yield Button("Limpar  ^L", id="clear-visible")
                        yield Button("Alternar  ^E", id="toggle-skill")
                        yield Button(
                            "Aplicar  ^A",
                            id="apply-skills",
                            variant="primary",
                        )
                with TabPane("Sobre", id="tab-about"):
                    yield Static(
                        f"[b]Specsfy CLI {__version__}[/b]\n\n"
                        "Framework para transformar ideias em especificações "
                        "rastreáveis e acompanhar sua entrega.\n\n"
                        "Skills instaladas são lidas do skills-lock.json na raiz "
                        "do projeto. Ctrl+Q encerra a interface.",
                        id="about-copy",
                    )
            yield Static("Carregando projeto…", id="status")
            yield Static(
                "^ = Ctrl  ·  Tab/Shift+Tab: foco  ·  Setas: navegar  ·  "
                "Espaço: abrir spec/alternar skill  ·  Esc: voltar  ·  "
                "Mouse: disponível",
                id="keyboard-help",
            )
        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one("#progress", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(
            "Spec",
            "Status",
            "Gates",
            "Tarefas",
            "Checklist",
            "Progresso",
        )
        backlog_table = self.query_one("#backlog-list", DataTable)
        backlog_table.cursor_type = "row"
        backlog_table.zebra_stripes = True
        backlog_table.add_column("Backlog")
        skills_table = self.query_one("#skills-table", DataTable)
        skills_table.cursor_type = "row"
        skills_table.zebra_stripes = True
        skills_table.add_columns("Plano", "Skill", "Categoria", "Estado")
        self.refresh_progress()
        await self.refresh_backlogs()
        await self.refresh_skills()
        interval = load_config(self._selected_project()).watch_interval
        self.set_interval(interval, self._refresh_if_changed)

    def _selected_project(self) -> Path:
        return Path(self.query_one("#project", Input).value).expanduser().resolve()

    async def _refresh_if_changed(self) -> None:
        try:
            project = self._selected_project()
        except NoMatches:
            return
        current = specs_fingerprint(project)
        if current != self._fingerprint:
            self.refresh_progress()
        current_backlogs = backlogs_fingerprint(project)
        if current_backlogs != self._backlog_fingerprint:
            await self.refresh_backlogs()
        current_lock = skills_lock_fingerprint(project)
        if current_lock != self._lock_fingerprint:
            await self.refresh_skills()

    def refresh_progress(self) -> None:
        project = self._selected_project()
        specs = scan_specs(project)
        self._specs = {spec.slug: spec for spec in specs}
        summary = summarize_specs(specs)
        table = self.query_one("#progress", DataTable)
        table.clear()
        for spec in specs:
            table.add_row(
                spec.slug,
                spec.status,
                f"{spec.passed_gates}/{spec.total_gates}",
                f"{spec.completed_tasks}/{spec.total_tasks}",
                f"{spec.completed_items}/{spec.total_items}",
                f"{_bar(spec.percent)} {spec.percent}%",
                key=spec.slug,
            )
        if specs:
            selected = (
                self._selected_spec_slug
                if self._selected_spec_slug in self._specs
                else specs[0].slug
            )
            self._selected_spec_slug = selected
            selected_index = next(
                index for index, spec in enumerate(specs) if spec.slug == selected
            )
            table.move_cursor(row=selected_index)
        else:
            self._selected_spec_slug = ""
        self.query_one("#summary-specs", Static).update(
            f"[b]{summary.total_specs}[/b]\nSpecs"
        )
        self.query_one("#summary-tasks", Static).update(
            f"[b]{summary.completed_tasks}/{summary.total_tasks}[/b]\n"
            f"Tarefas · {summary.pending_tasks} pendentes"
        )
        self.query_one("#summary-items", Static).update(
            f"[b]{summary.completed_items}/{summary.total_items}[/b]\n"
            f"Itens · {summary.pending_items} pendentes"
        )
        self.query_one("#summary-progress", Static).update(
            f"[b]{summary.percent}%[/b]\n{_bar(summary.percent, width=16)}"
        )
        state = (
            "nenhuma spec encontrada"
            if not specs
            else f"{summary.completed_specs}/{summary.total_specs} specs completas"
        )
        self.query_one("#status", Static).update(
            f"{project} · {state} · atualização automática ativa"
        )
        self._fingerprint = specs_fingerprint(project)

    async def refresh_backlogs(self) -> None:
        project = self._selected_project()
        items = scan_backlogs(project)
        self._backlogs = {item.slug: item for item in items}
        table = self.query_one("#backlog-list", DataTable)
        table.clear()
        for item in items:
            table.add_row(
                item.title,
                key=item.slug,
            )
        if items:
            selected = (
                self._selected_backlog_slug
                if self._selected_backlog_slug in self._backlogs
                else items[0].slug
            )
            self._selected_backlog_slug = selected
            selected_index = next(
                index for index, item in enumerate(items) if item.slug == selected
            )
            table.move_cursor(row=selected_index)
            await self._show_backlog(selected)
        else:
            self._selected_backlog_slug = ""
            self.query_one("#backlog-preview-title", Static).update(
                "Nenhum backlog"
            )
            await self.query_one("#backlog-preview", Markdown).update(
                "Crie arquivos em `specs/backlog/<NNNN>-<slug>.md` para "
                "visualizá-los aqui."
            )
        self.query_one("#backlog-list-title", Static).update(
            f"Backlogs · {len(items)}"
        )
        self._backlog_fingerprint = backlogs_fingerprint(project)

    async def on_data_table_row_highlighted(
        self,
        event: DataTable.RowHighlighted,
    ) -> None:
        key = str(event.row_key.value)
        if event.data_table.id == "backlog-list" and key in self._backlogs:
            self._selected_backlog_slug = key
            await self._show_backlog(key)
        elif event.data_table.id == "progress" and key in self._specs:
            self._selected_spec_slug = key
        elif event.data_table.id == "skills-table":
            self._selected_skill_name = key
            self._update_skill_detail()

    async def on_data_table_row_selected(
        self,
        event: DataTable.RowSelected,
    ) -> None:
        if event.data_table.id == "progress":
            self._selected_spec_slug = str(event.row_key.value)
            self.action_open_spec()
        elif event.data_table.id == "skills-table":
            self._selected_skill_name = str(event.row_key.value)
            await self.action_toggle_skill()

    async def _show_backlog(self, slug: str) -> None:
        item = self._backlogs[slug]
        self.query_one("#backlog-preview-title", Static).update(
            f"{item.identifier} · {item.status}"
        )
        await self.query_one("#backlog-preview", Markdown).update(
            _format_backlog_preview(item.content)
        )

    async def refresh_skills(self, *, reload_catalog: bool = False) -> None:
        project = self._selected_project()
        status = self.query_one("#skills-status", Static)
        table = self.query_one("#skills-table", DataTable)
        try:
            payload = ensure_skills_lock(project)
            installed = {
                name for name in payload["skills"] if _is_specsfy_skill(name)
            }
            entries = self._catalog_entries(reload=reload_catalog)
            self._installed_skills = installed
            self._selected_skills = set(installed)
            self._skill_options_cache = _skill_options(entries, installed)
            self._skills_initialized = True
            await self._render_skill_options()
            suffix = (
                f" · catálogo indisponível: {self._catalog_error}"
                if self._catalog_error
                else ""
            )
            status.update(
                f"{project / 'skills-lock.json'} · "
                f"{len(installed)} skill(s) Specsfy instalada(s){suffix}"
            )
            self._lock_fingerprint = skills_lock_fingerprint(project)
        except Exception as error:
            table.clear()
            self._selected_skill_name = ""
            self._update_skill_detail()
            status.update(f"Erro: {error}")
            self._lock_fingerprint = skills_lock_fingerprint(project)

    def _catalog_entries(self, *, reload: bool = False) -> list[CatalogEntry]:
        if reload:
            self._catalog = None
        if self._catalog is None:
            try:
                self._catalog = Catalog.fetch()
                self._catalog_error = ""
            except Exception as error:
                self._catalog_error = str(error)
                return []
        return self._catalog.entries

    async def _render_skill_options(self) -> None:
        if not self._skills_initialized:
            return
        table = self.query_one("#skills-table", DataTable)
        visible = self._visible_skill_options()
        table.clear()
        if not visible:
            self._selected_skill_name = ""
            self._update_skill_detail()
            self._update_selection_summary(visible_count=0)
            self.query_one("#skills-status", Static).update(
                "Nenhuma skill Specsfy corresponde à busca ou ao filtro."
            )
            return
        for option in visible:
            category = CATEGORY_LABELS.get(
                option.kind,
                option.kind.replace("-", " ").title(),
            )
            table.add_row(
                _skill_plan_label(
                    option.name,
                    self._installed_skills,
                    self._selected_skills,
                ),
                _friendly_skill_name(option.name),
                category,
                _skill_state_label(
                    option.name,
                    self._installed_skills,
                    self._detected_skills,
                ),
                key=option.name,
            )
        visible_names = [option.name for option in visible]
        selected = (
            self._selected_skill_name
            if self._selected_skill_name in visible_names
            else visible_names[0]
        )
        self._selected_skill_name = selected
        table.move_cursor(row=visible_names.index(selected))
        self._update_skill_detail()
        self._update_selection_summary(visible_count=len(visible))

    def _update_skill_detail(self) -> None:
        detail = self.query_one("#skill-detail", Static)
        toggle = self.query_one("#toggle-skill", Button)
        option = next(
            (
                candidate
                for candidate in self._skill_options_cache
                if candidate.name == self._selected_skill_name
            ),
            None,
        )
        if option is None:
            detail.update(
                "Nenhuma skill visível.\n\n"
                "Ajuste a busca ou os filtros para continuar."
            )
            toggle.disabled = True
            return
        category = CATEGORY_LABELS.get(
            option.kind,
            option.kind.replace("-", " ").title(),
        )
        states = [
            (
                "Instalada"
                if option.name in self._installed_skills
                else "Não instalada"
            )
        ]
        if option.name in self._detected_skills:
            states.append("Recomendada")
        plan = _skill_plan_label(
            option.name,
            self._installed_skills,
            self._selected_skills,
        )
        detail.update(
            f"{_friendly_skill_name(option.name)}\n"
            f"Plano: {plan} · Estado: {' · '.join(states)}\n"
            f"Categoria: {category}\n"
            f"{option.description}\n\n"
            f"ID: {option.name}"
        )
        toggle.disabled = False

    def _visible_skill_options(self) -> list[SkillOption]:
        query = self.query_one("#skills-search", Input).value.strip().casefold()
        visible = []
        for option in self._skill_options_cache:
            if query and query not in " ".join(
                (option.name, option.description, option.kind)
            ).casefold():
                continue
            if self._skill_filter == "installed" and (
                option.name not in self._installed_skills
            ):
                continue
            if self._skill_filter == "detected" and (
                option.name not in self._detected_skills
            ):
                continue
            if self._skill_filter == "base" and option.kind != "base":
                continue
            if self._skill_filter == "specialists" and option.kind == "base":
                continue
            visible.append(option)
        return visible

    def _update_selection_summary(self, *, visible_count: int | None = None) -> None:
        selected = self._selected_skills
        to_install = selected - self._installed_skills
        to_remove = self._installed_skills - selected
        visible = (
            visible_count
            if visible_count is not None
            else len(self._visible_skill_options())
        )
        self.query_one("#skills-selection-summary", Static).update(
            f"[b]{len(selected)} selecionada(s)[/b] · {visible} visível(is) · "
            f"[#56d364]{len(to_install)} para instalar[/] · "
            f"[#ff7b72]{len(to_remove)} para remover[/]"
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh":
            await self.action_refresh()
        elif event.button.id == "install":
            await self.action_install_base()
        elif event.button.id == "detect":
            await self.action_detect_skills()
        elif event.button.id == "toggle-skill":
            await self.action_toggle_skill()
        elif event.button.id == "apply-skills":
            await self.action_apply_skills()
        elif event.button.id == "update-skills":
            await self.action_update_skills()
        elif event.button.id == "run-tests":
            self.action_run_tests()
        elif event.button.id == "select-visible":
            await self.action_select_visible()
        elif event.button.id == "clear-visible":
            await self.action_clear_visible()
        elif event.button.id and event.button.id.startswith("filter-"):
            await self._set_skill_filter(event.button.id.removeprefix("filter-"))

    async def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "skills-search":
            await self._render_skill_options()

    async def _set_skill_filter(self, filter_name: str) -> None:
        self._skill_filter = filter_name
        for button in self.query("#skills-filters Button"):
            button.variant = (
                "primary" if button.id == f"filter-{filter_name}" else "default"
            )
        await self._render_skill_options()

    async def action_filter_all(self) -> None:
        await self._set_skill_filter("all")

    async def action_filter_installed(self) -> None:
        await self._set_skill_filter("installed")

    async def action_filter_detected(self) -> None:
        await self._set_skill_filter("detected")

    async def action_refresh(self) -> None:
        self.refresh_progress()
        await self.refresh_backlogs()
        await self.refresh_skills(reload_catalog=True)

    async def action_install_base(self) -> None:
        self._show_tab("tab-skills")
        self._selected_skills.update(FRAMEWORK_SKILLS)
        await self._render_skill_options()
        self.query_one("#skills-status", Static).update(
            "As skills do framework foram selecionadas. Use Aplicar seleção."
        )

    async def action_detect_skills(self) -> None:
        self._show_tab("tab-skills")
        try:
            entries = self._catalog_entries(reload=True)
            detected = {
                entry.name
                for entry in Catalog(entries).detect(self._selected_project())
            }
            self._detected_skills = detected
            self._selected_skills.update(detected)
            self._skill_options_cache = _skill_options(
                entries,
                self._installed_skills,
            )
            await self._set_skill_filter("detected")
            message = ", ".join(sorted(detected)) if detected else "nenhuma skill"
            self.query_one("#skills-status", Static).update(
                f"Skills detectadas e selecionadas: {message}"
            )
        except Exception as error:
            self.query_one("#skills-status", Static).update(f"Erro: {error}")

    async def action_clear_visible(self) -> None:
        self._selected_skills.difference_update(
            option.name for option in self._visible_skill_options()
        )
        await self._render_skill_options()

    async def action_select_visible(self) -> None:
        self._selected_skills.update(
            option.name for option in self._visible_skill_options()
        )
        await self._render_skill_options()

    async def action_toggle_skill(self) -> None:
        tabs = self.query_one("#workspace-tabs", TabbedContent)
        if tabs.active != "tab-skills":
            return
        name = self._selected_skill_name
        if not name:
            return
        if name in self._selected_skills:
            self._selected_skills.remove(name)
        else:
            self._selected_skills.add(name)
        await self._render_skill_options()

    async def action_activate_selection(self) -> None:
        tabs = self.query_one("#workspace-tabs", TabbedContent)
        if tabs.active == "tab-specs":
            self.action_open_spec()
        elif tabs.active == "tab-skills":
            await self.action_toggle_skill()

    def action_open_spec(self) -> None:
        spec = self._specs.get(self._selected_spec_slug)
        if spec is None:
            return
        self.push_screen(SpecPreviewModal(spec))

    async def action_apply_skills(self) -> None:
        project = self._selected_project()
        try:
            installed = {
                name
                for name in installed_skill_names(project)
                if _is_specsfy_skill(name)
            }
            selected = {
                name for name in self._selected_skills if _is_specsfy_skill(name)
            }
            selected_specialists = sorted(
                name
                for name in selected
                if name.startswith("specsfy-specialist-")
            )
            catalog: Catalog | None = None
            required_specialists: set[str] = set()
            if selected_specialists:
                catalog = Catalog(self._catalog_entries())
                catalog_names = {entry.name for entry in catalog.entries}
                required_specialists = {
                    entry.name
                    for entry in catalog.resolve(
                        [
                            name
                            for name in selected_specialists
                            if name in catalog_names
                        ]
                    )
                }
            selected.update(required_specialists)
            self._selected_skills.update(required_specialists)
            to_add = selected - installed
            to_remove = installed - selected
            base = sorted(to_add & set(FRAMEWORK_SKILLS))
            specialists = sorted(
                name
                for name in to_add
                if name.startswith("specsfy-specialist-")
            )
            installer = SkillInstaller(project)
            changed: list[Path] = []
            if base:
                changed.extend(installer.install_base_selection(base))
            if specialists:
                catalog = catalog or Catalog(self._catalog_entries())
                validated = [
                    entry.name
                    for entry in catalog.resolve(specialists)
                    if entry.name not in installed
                ]
                changed.extend(installer.install_specialists(validated))
            if to_remove:
                changed.extend(installer.remove(sorted(to_remove)))
            await self.refresh_skills()
            message = (
                f"Seleção aplicada: {len(changed)} alteração(ões)."
                if changed
                else "A seleção já corresponde ao skills-lock.json."
            )
            self.query_one("#skills-status", Static).update(message)
        except Exception as error:
            self.query_one("#skills-status", Static).update(f"Erro: {error}")

    async def action_update_skills(self) -> None:
        self._show_tab("tab-skills")
        try:
            changed = SkillInstaller(self._selected_project()).update_all()
            await self.refresh_skills(reload_catalog=True)
            message = (
                f"Skills atualizadas: {len(changed)} alteração(ões)."
                if changed
                else "Todas as skills instaladas já estão atualizadas."
            )
            self.query_one("#skills-status", Static).update(message)
        except Exception as error:
            self.query_one("#skills-status", Static).update(f"Erro: {error}")

    def action_run_tests(self):
        self._show_tab("tab-tests")
        if self._test_worker is not None and self._test_worker.is_running:
            return self._test_worker
        self._test_worker = self.run_worker(
            self._run_project_tests(),
            name="project-tests",
            group="project-tests",
            exit_on_error=False,
        )
        return self._test_worker

    async def _run_project_tests(self) -> TestRun | None:
        project = self._selected_project()
        status = self.query_one("#tests-status", Static)
        summary = self.query_one("#tests-summary", Static)
        output = self.query_one("#tests-output", RichLog)
        button = self.query_one("#run-tests", Button)
        tabs = self.query_one("#test-results-tabs", TabbedContent)
        output.clear()
        summary.update(
            f"Projeto: {project}\n\nPreparando o runner de testes…"
        )
        status.update("Executando os testes do projeto…")
        tabs.active = "tab-tests-output"
        button.disabled = True
        try:
            result = await stream_project_tests(project, emit=output.write)
            state = "Testes passaram" if result.exit_code == 0 else "Testes falharam"
            status.update(
                f"{state} · {result.duration_seconds:.2f}s · "
                f"exit code {result.exit_code}"
            )
            summary.update(_format_test_run(result))
            tabs.active = "tab-tests-summary"
            return result
        except (ValueError, RuntimeError, OSError) as error:
            message = f"Erro ao executar testes: {error}"
            status.update(message)
            summary.update(message)
            output.write(message)
            tabs.active = "tab-tests-summary"
            return None
        finally:
            button.disabled = False

    def action_show_home(self) -> None:
        self._show_tab("tab-home")

    def action_show_backlogs(self) -> None:
        self._show_tab("tab-backlogs")
        self.query_one("#backlog-list", DataTable).focus()

    def action_show_specs(self) -> None:
        self._show_tab("tab-specs")
        self.query_one("#progress", DataTable).focus()

    def action_show_tests(self) -> None:
        self._show_tab("tab-tests")
        self.query_one("#run-tests", Button).focus()

    def action_show_skills(self) -> None:
        self._show_tab("tab-skills")
        self.query_one("#skills-table", DataTable).focus()

    def action_show_about(self) -> None:
        self._show_tab("tab-about")

    def action_back(self) -> None:
        if isinstance(self.screen, SpecPreviewModal):
            self.screen.dismiss()
            return
        search = self.query_one("#skills-search", Input)
        tabs = self.query_one("#workspace-tabs", TabbedContent)
        if tabs.active == "tab-skills" and search.value:
            search.value = ""
            return
        if tabs.active != "tab-home":
            tabs.active = "tab-home"

    def _show_tab(self, tab_id: str) -> None:
        self.query_one("#workspace-tabs", TabbedContent).active = tab_id


def _format_test_run(result: TestRun) -> str:
    state = "PASSOU" if result.exit_code == 0 else "FALHOU"
    details = "\n".join(result.summary_lines) or "O runner não emitiu um resumo."
    return (
        f"{state}\n\n"
        f"Runner: {result.command.label}\n"
        f"Comando: {result.command.display}\n"
        f"Projeto: {result.command.cwd}\n"
        f"Duração: {result.duration_seconds:.2f}s\n"
        f"Exit code: {result.exit_code}\n\n"
        f"{details}"
    )


def _skill_options(
    catalog_entries: list[CatalogEntry],
    installed: set[str],
) -> list[SkillOption]:
    options = [
        SkillOption(
            name=name,
            description=BASE_DESCRIPTIONS[name],
            kind="base",
            installed=name in installed,
        )
        for name in FRAMEWORK_SKILLS
    ]
    options = [
        SkillOption(
            name=option.name,
            description=option.description,
            kind=(
                "auxiliary"
                if option.name in AUXILIARY_SKILLS or option.name == "specsfy-setup"
                else "documentation"
                if option.name in DOCUMENTATION_SKILLS
                else option.kind
            ),
            installed=option.installed,
        )
        for option in options
    ]
    known = set(FRAMEWORK_SKILLS)
    for entry in catalog_entries:
        known.add(entry.name)
        options.append(
            SkillOption(
                name=entry.name,
                description=entry.description,
                kind=entry.category,
                installed=entry.name in installed,
            )
        )
    for name in sorted(installed - known):
        if not _is_specsfy_skill(name):
            continue
        options.append(
            SkillOption(
                name=name,
                description="Skill Specsfy instalada fora do catálogo atual.",
                kind="instalada",
                installed=True,
            )
        )
    order = {name: index for index, name in enumerate(CATEGORY_LABELS)}
    return sorted(
        options,
        key=lambda option: (order.get(option.kind, len(order)), option.name),
    )


def _is_specsfy_skill(name: str) -> bool:
    return (
        name == "specsfy-setup"
        or name in DOCUMENTATION_SKILLS
        or name.startswith("specsfy-aux-")
        or name.startswith("specsfy-base-")
        or name.startswith("specsfy-specialist-")
    )


def _friendly_skill_name(name: str) -> str:
    if name == "specsfy-setup":
        return "Setup"
    if name in DOCUMENTATION_SKILLS:
        return "Documentator"
    for prefix in ("specsfy-aux-", "specsfy-base-", "specsfy-specialist-"):
        if name.startswith(prefix):
            return name.removeprefix(prefix).replace("-", " ").title()
    return name.replace("-", " ").title()


def _skill_plan_label(
    name: str,
    installed: set[str],
    selected: set[str],
) -> str:
    if name in selected:
        return "Manter" if name in installed else "Instalar"
    return "Remover" if name in installed else "Ignorar"


def _skill_state_label(
    name: str,
    installed: set[str],
    detected: set[str],
) -> str:
    states = ["Instalada" if name in installed else "Disponível"]
    if name in detected:
        states.append("Recomendada")
    return " · ".join(states)


def _format_backlog_preview(content: str) -> str:
    lines = []
    for line in content.splitlines():
        if line.startswith("**") and "**:" in line and not line.endswith("  "):
            line += "  "
        lines.append(line)
    return "\n".join(lines)


def _bar(percent: int, width: int = 10) -> str:
    filled = round(percent * width / 100)
    return "█" * filled + "░" * (width - filled)
