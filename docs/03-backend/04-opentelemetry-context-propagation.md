# OpenTelemetry Context Propagation & Baggage

## Mental model
Propagator process boundary'de context'i carrier'a inject eder ve karşı tarafta extract eder. Baggage trace context'ten ayrı key/value context'tir ve span attribute değildir.

```text
Context A -> inject -> HTTP/queue headers -> extract -> Context B -> child span
```

## Trust boundary
Baggage wire üzerinde taşınabilir, loglanabilir ve built-in integrity garantisi yoktur. PII, credential ve authorization kararlarını baggage'a bağlama. Public ingress'te untrusted propagation context'ini sanitize/ignore et; third-party egress'te internal context sızıntısını kontrol et.

## Interview depth
Mid: trace/span/context ve inject/extract. Senior: async boundaries, baggage, sampling ve trust boundaries. Staff: propagation policy, egress filtering ve telemetry governance.

## Production failure modes
Async context loss, yanlış parent, yüksek-cardinality baggage, sensitive-data leakage ve forged headers'ı business identity sanmak.

## Kaynaklar
- https://opentelemetry.io/docs/specs/otel/context/api-propagators/
- https://opentelemetry.io/docs/concepts/context-propagation/
- https://opentelemetry.io/docs/concepts/signals/baggage/
