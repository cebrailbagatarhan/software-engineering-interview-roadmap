# OpenTelemetry Logs, Events & Trace Correlation

## Konu anlatımı
OpenTelemetry Logs Data Model structured log kayıtlarını ortak semantik alanlarla temsil eder: `Timestamp`, `ObservedTimestamp`, `TraceId`, `SpanId`, `SeverityText`, `SeverityNumber`, `Body`, `Resource`, `InstrumentationScope`, `Attributes` ve `EventName`. Trace/span kimlikleri log→trace correlation sağlar.

Non-empty `EventName` taşıyan LogRecord bir Event'tir. Named event belirli bir occurrence ve şema için; serbest diagnostic mesaj normal log için uygundur. Production tasarımında cardinality, PII/secrets, retention ve ingestion maliyeti telemetry şeması kadar önemlidir.

## Mental model
```text
request
  +--> span(trace_id=T, span_id=S)
  +--> log{TraceId=T, SpanId=S, Severity=ERROR}
                    |
                    v
              correlated view
```

## Mülakat soruları
- `Timestamp` ve `ObservedTimestamp` farkı?
- `SeverityText` ve normalize `SeverityNumber` neden birlikte bulunur?
- Log-trace correlation nasıl çalışır?
- Event ile diagnostic log ne zaman ayrılır?
- Resource ve occurrence attributes farkı?
- Staff: cardinality, redaction, retention ve sampling governance nasıl kurulur?

## Beklenen cevap seviyesi
Mid: structured logs/severity/correlation. Senior: resource/scope/event, ingestion, cardinality, redaction. Staff: schema governance, cost controls, retention tiers ve incident ergonomics.

## Mini alıştırma
Checkout failure için LogRecord tasarla; Resource/Attributes/EventName ayrımını yap ve bir secret'ın redaction noktasını belirt.

## Proje fikri
`otel-log-correlation-lab`: HTTP trace + structured logs üret, Collector'a gönder ve TraceId üzerinden log→trace pivot'u göster.

## Production / failure modes
Sınırsız high-cardinality attribute; secret/PII sızıntısı; tutarsız severity mapping; correlation alanlarının kaybı; parse edilmesi gereken dev Body string'leri.

## Kaynaklar
- https://opentelemetry.io/docs/specs/otel/logs/data-model/
- https://opentelemetry.io/docs/specs/semconv/general/events/
- https://opentelemetry.io/docs/concepts/signals/logs/
