# OpenTelemetry Stable Database Semantic Conventions

## Konu anlatımı
Telemetry schema producer ile dashboard, alert ve query tüketicileri arasında contract'tır. OpenTelemetry genel database client span conventions'ı stable durumdadır ve `db.system.name`, `db.namespace`, `db.collection.name`, `db.operation.name`, `db.query.summary` gibi ortak alanlarla vendorlar arası sorgulanabilirlik hedefler.

## Mental model
```text
instrumentation -> semantic contract -> collector/backend -> dashboards/alerts
                       |
                 schema migration
```

## Migration
Eski experimental conventions kullanan mevcut instrumentation major version'ları için `OTEL_SEMCONV_STABILITY_OPT_IN=database` stable convention'a geçişi, `database/dup` ise phased dual emission'ı destekler. Dual emission geçici migration aracıdır; süresiz bırakmak telemetry cost'u artırır.

## Internals / security
Database operation span'i genellikle `CLIENT` kind'dır. `db.query.summary` mevcutsa span name için tercih edilir. Raw SQL'in kontrolsüz kaydı cardinality, PII/secrets ve maliyet riski taşır. `db.client.operation.duration` stable histogram metriğidir; connection-pool metriklerinin bazıları Development statüsündedir.

## Mülakat odağı
- Semantic convention neden contract?
- Low-cardinality summary vs raw statement
- Stable schema migration ve dashboard compatibility
- Dual emission window
- Span + metric correlation
- Fleet-wide governance ve telemetry economics

## Alıştırma / proje
Eski `db.system`/`db.name` dashboard'larını inventory et; dual emission -> consumer migration -> old field retirement planı yaz. PostgreSQL client ile stable spans/metrics ve cardinality guard içeren küçük lab kur.

## Failure modes / production
Big-bang rename, raw SQL ile PII/cardinality, stable/development alanları karıştırmak, dual emission'ı süresiz tutmak. Series cardinality, telemetry bytes, dashboard query error ve migration coverage izle.

## Kaynaklar
- https://opentelemetry.io/docs/specs/semconv/db/database-spans/
- https://opentelemetry.io/docs/specs/semconv/db/database-metrics/
- https://opentelemetry.io/docs/specs/semconv/db/sql/
- https://opentelemetry.io/docs/specs/otel/versioning-and-stability/
