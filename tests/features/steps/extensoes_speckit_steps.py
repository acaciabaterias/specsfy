from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from behave import given, then, when


ROOT = Path(__file__).resolve().parents[3]
TEST_FILE = ROOT / "tests" / "test_extensoes_speckit.py"
CONTRACTS = {
    "gate-parity": "test_gate_parity_attestation_and_canaries",
    "evidence-chain": "test_evidence_and_full_trace_chain",
    "research": "test_research_loader_and_claim_gate",
    "change": "test_change_impact_and_changelog",
    "reviews": "test_review_findings_contract",
    "qa": "test_acceptance_audit",
    "context": "test_context_analysis_labels_sources",
    "delivery": "test_delivery_renderer_requires_gate",
}


@given("o contrato de adaptações Spec Kit")
def given_extension_contract(context) -> None:
    context.root = ROOT


@when('executo o contrato focal "{name}"')
def when_extension_contract(context, name: str) -> None:
    method = CONTRACTS[name]
    context.result = subprocess.run(
        [
            sys.executable,
            str(TEST_FILE),
            f"ExtensionAdaptationTests.{method}",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


@then("o contrato focal passa")
def then_extension_contract_passes(context) -> None:
    assert context.result.returncode == 0, (
        context.result.stdout + context.result.stderr
    )

