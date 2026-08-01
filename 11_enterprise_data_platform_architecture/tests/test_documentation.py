from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_architecture_artifacts_exist():
    required = [
        "architecture/logical_architecture.md",
        "architecture/physical_azure_architecture.md",
        "architecture/security_boundaries.md",
        "reliability/service_level_objectives.md",
        "disaster_recovery/disaster_recovery_strategy.md",
        "contracts/examples/public_health_event_contract.json",
        "runbooks/critical_daily_publication_runbook.md",
    ]
    assert all((ROOT / path).exists() for path in required)


def test_all_adrs_use_required_sections():
    required = ["## Status", "## Context", "## Decision"]
    for path in (ROOT / "architecture_decision_records").glob("ADR_*.md"):
        text = path.read_text(encoding="utf-8")
        assert all(section in text for section in required), path


def test_no_macos_metadata_is_packaged():
    bad = {".DS_Store", "__MACOSX"}
    assert not any(path.name in bad for path in ROOT.rglob("*"))
