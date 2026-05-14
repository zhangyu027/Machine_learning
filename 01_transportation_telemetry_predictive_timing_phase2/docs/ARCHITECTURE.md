# Architecture

```text
Train telemetry sensors
        ↓
Kafka / Kinesis concept
        ↓
Spark / Flink concept
        ↓
Bronze: raw immutable events
        ↓
Silver: cleansed telemetry records
        ↓
Gold: ML-ready certified feature table
        ↓
Neural network predictive timing model
        ↓
Dashboards and operations analytics
```

## Reliability concepts

- event time vs processing time
- late-arriving events
- checkpointing
- replayable topics
- deduplication
- schema evolution
- SLA monitoring
