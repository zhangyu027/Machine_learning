from enterprise_data_platform.contracts import DataContract, validate_record


def test_contract_validates_required_and_allowed_values():
    contract = DataContract.from_dict({
        "dataset": "d.x", "version": "1", "grain": ["id"], "freshness_hours": 24,
        "fields": [{"name": "id", "type": "string", "required": True},
                   {"name": "status", "type": "string", "allowed_values": ["A"]}],
    })
    assert validate_record({"id": "1", "status": "A"}, contract) == []
    assert validate_record({"id": "", "status": "B"}, contract)
