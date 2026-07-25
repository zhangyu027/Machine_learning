from __future__ import annotations

from contextlib import nullcontext


def configure_tracing(app, enabled: bool = False):
    if not enabled:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        provider = TracerProvider(resource=Resource.create({"service.name": "siri-rag-api"}))
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
        trace.set_tracer_provider(provider)
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        # Tracing remains optional so local use does not fail when no collector exists.
        return


def span(name: str):
    try:
        from opentelemetry import trace
        return trace.get_tracer("siri-rag").start_as_current_span(name)
    except Exception:
        return nullcontext()
