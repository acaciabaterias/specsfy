from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
METHODS = {
    "attested-evidence": "test_attestation_binds_commit_task_and_file_hashes",
    "policy-digest": "test_policy_digest_covers_commands_limits_and_sources",
    "attested-qa": "test_acceptance_audits_runner_attestation",
    "immutable-ci": "test_ci_dependencies_are_immutably_pinned",
    "runner-limits": "test_runner_times_out_and_truncates_output",
    "finding-integrity": "test_findings_validate_identity_refs_and_evidence",
    "research-integrity": "test_research_validates_ids_budgets_and_anchors",
    "semantic-impact": "test_change_impact_uses_semantic_section_titles",
}


@given("o contrato de robustez das extensões")
def given_robustness_contract(context) -> None:
    context.root = ROOT


@when('executo o contrato de robustez "{name}"')
def when_run_robustness_contract(context, name: str) -> None:
    method = METHODS[name]
    context.result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            f"tests.test_robustez_extensoes.RobustnessImprovementTests.{method}",
        ],
        cwd=context.root,
        text=True,
        capture_output=True,
        check=False,
    )


@then("o contrato de robustez passa")
def then_robustness_contract_passes(context) -> None:
    assert context.result.returncode == 0, (
        context.result.stdout + context.result.stderr
    )
