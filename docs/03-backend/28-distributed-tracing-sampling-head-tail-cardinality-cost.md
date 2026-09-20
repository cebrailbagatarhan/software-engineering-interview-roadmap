# Distributed Tracing Sampling — Head, Tail, Cardinality ve Cost

## Mental model
```text
head: request -> early keep/drop -> spans -> backend

tail: spans -> trace-aware collector -> buffer -> policy -> backend
                                      error? slow?

signal quality <---- trade-off ----> telemetry cost
```

Sampling observability signal ile ingestion/storage cost arasında kontrollü kayıp yaratır. Head sampling trace başında ucuz karar verir fakat future error/latency sonucunu bilemez. Tail sampling trace hakkında daha fazla bilgi gördükten sonra error/slow-trace gibi policies uygulayabilir; bunun bedeli buffering, memory, decision latency ve trace-affinity'dir. OpenTelemetry Collector probabilistic ve tail sampling processor'larını destekler.

## Internals
- Head sampling telemetry hacmini kaynağa yakın azaltabilir.
- Tail sampling state tutar ve trace tamamlanmasını bekler.
- Aynı trace'in span'ları aynı decision point'e ulaşmalıdır; aksi halde fragmented context oluşur.
- Error/latency policy rare-but-important traces'i koruyabilir.
- Sampling metric yerine geçmez; sampled traces üzerinden doğrudan SLO/request count çıkarmak bias yaratabilir.
- Attribute cardinality ayrı bir cost/privacy eksenidir.

## Mülakat soruları
1. Head ve tail sampling farkı nedir?
2. Random %1 neden tüm incident'lar için yeterli değildir?
3. Tail sampling neden memory ister?
4. Trace affinity neden önemlidir?
5. Staff: errors + slow traces + random baseline policy nasıl tasarlanır?
6. Principal: telemetry budget, privacy ve debugging coverage nasıl yönetilir?

## Seviye beklentisi
Mid sampling/cost; Senior buffering/bias/completeness; Staff collector topology/backpressure/cardinality; Principal telemetry economics, retention, privacy ve platform governance açıklamalıdır.

## Alıştırma ve proje
100k req/s ve trace başına 20 KiB için ham throughput'u ve %1 sampling sonrası hacmi hesapla. Üç servisli OpenTelemetry demo kurup probabilistic ve tail policies ile kept traces, collector memory, decision latency ve ingest hacmini karşılaştır.

## Failure modes / production
Aggressive sampling incident evidence'ı silebilir; tail sampler overload/drop yaşayabilir; yanlış routing trace parçalayabilir; high-cardinality attributes maliyeti büyütebilir. Collector memory/queue, dropped spans, export errors, sampling ratios, decision latency ve telemetry spend izle.

## Kaynaklar
- https://opentelemetry.io/docs/concepts/sampling/
- https://opentelemetry.io/docs/collector/
- https://opentelemetry.io/docs/collector/components/processor/
