import json
from pathlib import Path

from enterprise_data_platform.pipeline import run_pipeline


def test_reference_pipeline_creates_governance_artifacts(tmp_path: Path):
    source = tmp_path / "input.jsonl"
    source.write_text('{"record_id":"1","domain":"Finance","status":"open","amount":10}\n', encoding="utf-8")
    contract = tmp_path / "contract.json"
    contract.write_text(json.dumps({
        "dataset":"finance.event","version":"1","grain":["record_id"],"freshness_hours":24,
        "fields":[
            {"name":"record_id","type":"string","required":True},
            {"name":"domain","type":"string","required":True},
            {"name":"status","type":"string","required":True,"allowed_values":["open","OPEN"]},
            {"name":"amount","type":"number","required":True}
        ]}), encoding="utf-8")
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"input_path":str(source),"contract_path":str(contract),"output_root":str(tmp_path/"out")}), encoding="utf-8")
    result = run_pipeline(config)
    assert result["status"] == "completed"
    assert (tmp_path / "out" / "lineage_manifest.json").exists()
    assert json.loads((tmp_path / "out" / "gold.json").read_text())[0]["total_amount"] == 10.0
