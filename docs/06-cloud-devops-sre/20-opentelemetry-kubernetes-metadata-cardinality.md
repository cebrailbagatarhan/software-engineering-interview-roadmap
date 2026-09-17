# OpenTelemetry Kubernetes Metadata Enrichment, Cardinality & Stable Semantics

## Neden önemli?
Kubernetes üzerinde telemetry'nin production değeri, sinyali doğru workload kimliğiyle ilişkilendirebilmeye bağlıdır. OpenTelemetry Kubernetes Attributes Processor telemetry resource'larını pod, namespace, deployment ve node metadata'sıyla zenginleştirir. Processor 16 Eylül 2026'da v1.0.0 milestone'una ulaştı.

## Mental model
```text
OTLP -> Collector -> k8sattributes -> filter/batch -> backend
                         |
                         +-> pod metadata cache <- Kubernetes API
```

Bu bir metadata join problemidir. Association doğruluğu, RBAC, cache freshness ve Collector deployment topology'si enrichment sonucunu belirler.

## Cardinality ekonomisi
Her metadata alanını metric dimension yapmak güvenli değildir. `namespace`, `deployment` gibi bounded alanlar genellikle değerlidir; `request_id`, `customer_id` veya serbest biçimli annotation'lar series sayısını patlatabilir. Metadata politikası allowlist, privacy classification ve backend cost budget ile yönetilmelidir.

## Mülakat derinliği
- Mid: resource attribute, label ve cardinality kavramlarını açıkla.
- Senior: pod association, RBAC/API outage ve DaemonSet-vs-gateway topology trade-off'larını tartış.
- Staff: semantic-convention migration, multi-tenant privacy ve org-wide metadata contract tasarla.

## Failure modes
Stale cache, yanlış pod association, unbounded label cardinality, PII leakage, aşırı Kubernetes API watch yükü ve semantic-name drift.

## Production bağlantısı
Series cardinality, enrichment miss rate, telemetry byte volume, Collector CPU/RSS, Kubernetes API errors ve ingest cost birlikte izlenmelidir.

## Kaynaklar
- https://opentelemetry.io/blog/2026/k8s-attributes-processor-v1/
- https://opentelemetry.io/docs/platforms/kubernetes/collector/components/
- https://opentelemetry.io/docs/specs/semconv/resource/k8s/
