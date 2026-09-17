# OpenTelemetry Profiles, eBPF & Cross-Signal Correlation

OpenTelemetry Profiles signal 26 Mart 2026'da public Alpha'ya geçti. Continuous production profiling, metrics/traces/logs'un yanına code-path ve on/off-CPU davranışını ekler.

```text
process -> profiler/eBPF -> stack samples -> symbolization -> profile store
                            |                       |
                            +-- trace/span context -+
```

## Mental model
Metrics `ne kadar`, traces `hangi request yolu`, logs `hangi olay`, profiles ise `hangi stack CPU tüketti veya bekledi` sorusuna odaklanır. eBPF düşük-intrusion system-level collection sağlayabilir; fakat symbolization, process/thread context ve correlation ayrı sistem problemleridir.

## Mülakat omurgası
- Sampling vs instrumentation profiling.
- On-CPU vs off-CPU.
- eBPF'nin avantaj ve sınırları.
- Symbolization ve build-ID/debug-symbol lifecycle.
- Trace/profile correlation.
- Alpha maturity'nin production riski.

## Production trade-off
Daha hızlı incident diagnosis ve compute optimization karşılığında ingest/storage cost, profiler overhead, cardinality ve immature-schema riski gelir. Profiler overhead, sample loss, symbolization success, ingest bytes ve correlated-profile ratio izlenmelidir.

## Alıştırma
CPU ortalaması değişmeden p99 kötüleşen servis için lock wait, endpoint CPU hotspot ve downstream wait hipotezlerini trace/profile/metric kanıtlarıyla ayır.

## Proje
CPU hotspot ve lock wait enjekte edilen serviste trace + metric + profile topla; `latency -> span -> stack` drill-down prototipi oluştur.

## Kaynaklar
- https://opentelemetry.io/blog/2026/profiles-alpha/
- https://opentelemetry.io/docs/specs/status/
