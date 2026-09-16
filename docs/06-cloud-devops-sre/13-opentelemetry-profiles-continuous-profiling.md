# OpenTelemetry Profiles: Continuous Profiling & Cross-Signal Correlation

OpenTelemetry Profiles 26 Mart 2026'da public Alpha'ya geçti. Profiling sinyali traces, metrics ve logs ile aynı telemetry ekosisteminde kod seviyesinde resource consumption görünürlüğü sağlamayı hedefler.

```text
trace --------+
metrics ------+--> shared resource/context --> diagnosis
logs ---------+
profiles -----+
```

## Profile neyi cevaplar?
Trace request'in sistemdeki causal path'ini gösterir. Profile ise CPU veya off-CPU sample'larının stack'ler üzerinde nasıl dağıldığını gösterir. Birlikte kullanıldıklarında 'hangi request yavaş?' sorusundan 'o request sırasında hangi kod CPU tüketti veya nerede bekledi?' sorusuna geçilebilir.

## Pipeline
Collector profiling verisini alabilir, Kubernetes metadata ile enrich edebilir ve OTTL ile transform/filter uygulayabilir. eBPF profiler düşük-instrumentation yaklaşımı sunar; backend tarafında OTLP Profiles desteği gerekir. Symbolization doğru function/source attribution için kritiktir.

## Trade-off'lar
Profiles Alpha maturity seviyesindedir; kritik production dependency olarak konumlandırmadan önce compatibility ve fallback düşünülmelidir. Sampling overhead, symbol storage/build IDs, privacy, cardinality ve retention cost ayrıca tasarlanmalıdır.

## Mülakat ekseni
CPU ve off-CPU profiling farkı nedir? Symbolization neden gerekir? Trace-profile correlation nasıl çalışır? eBPF'nin sınırları nelerdir? Staff seviyesinde ingestion, retention ve cost budget nasıl tasarlanır?

## Production sinyalleri
Agent CPU/RSS overhead, dropped samples, symbolization success, ingest bytes, retention cost ve trace-profile correlation coverage izlenmelidir.

## Kaynaklar
- https://opentelemetry.io/blog/2026/profiles-alpha/
- https://opentelemetry.io/docs/concepts/signals/profiles/
- https://opentelemetry.io/docs/specs/otel/profiles/
