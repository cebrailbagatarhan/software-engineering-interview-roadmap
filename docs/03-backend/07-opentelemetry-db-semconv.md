# OpenTelemetry Database Semantic Conventions

## Mental model
```text
DB call -> CLIENT span -> stable semantic attributes
                      -> useful grouping
                      -> privacy/cardinality constraints
```

OpenTelemetry database semantic conventions polyglot sistemlerde database client operasyonlarını ortak attribute ve span semantics ile ifade eder. `db.system.name`, `db.operation.name`, `db.query.summary` ve ilgili namespace/target alanları analiz edilebilir ortak bir telemetry contract sağlar. Raw query ve parameter capture privacy ile cardinality riski taşır; query text sanitization ve düşük-cardinality summary production tasarımının parçasıdır.

## Mülakat odağı
- Semantic convention neden gerekir?
- CLIENT span neyi temsil eder?
- Query summary vs query text.
- PII, sanitization ve high-cardinality maliyeti.
- Convention migration ve dashboard compatibility.

## Mini alıştırma
Bir checkout PostgreSQL çağrısı için güvenli span schema tasarla; capture etmeyeceğin alanları gerekçelendir.

## Failure modes / production
PII sızıntısı; user-id gibi high-cardinality labels; version migration'da dashboard kırılması; telemetry storage maliyetini görmezden gelmek.

## Kaynaklar
- https://opentelemetry.io/docs/specs/semconv/db/database-spans/
- https://opentelemetry.io/docs/specs/semconv/db/sql/
- https://opentelemetry.io/docs/specs/otel/trace/api/
