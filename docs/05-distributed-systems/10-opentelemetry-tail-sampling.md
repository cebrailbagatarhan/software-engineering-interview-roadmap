# OpenTelemetry Tail Sampling, Cost & Failure Visibility

## Mental model
```text
trace start -> head decision -> services -> collector buffer -> tail policy -> export/drop
                                             error? slow? critical?
```

Head sampling erken, ucuz ve outcome'a kördür. Tail sampling trace hakkında daha fazla span/outcome gördükten sonra karar verebildiği için rare error veya slow trace'leri seçebilir; bunun karşılığında collector state, memory ve decision latency gerekir.

OpenTelemetry Collector receive/process/export pipeline sağlar ve probabilistic ile tail sampling processor'larını destekler. Head ve tail birlikte kullanılabilir; ancak head aşamasında atılan trace downstream tail sampler tarafından geri getirilemez.

## Production trade-off
Tail sampling capacity problemi aynı zamanda observability correctness problemidir. Collector overload veya incomplete trace kararları incident visibility'yi bozabilir. Trace affinity, decision window, queue/memory capacity ve collector self-observability tasarımın parçasıdır. Sampling privacy/redaction kontrolü değildir.

## Mülakat soruları
- Head ve tail sampling trade-off'u nedir?
- Tail sampler neden state tutar?
- Rare errors nasıl korunur?
- Horizontal scaling'de trace affinity neden önemlidir?
- Telemetry cost budget ile incident riskini nasıl dengelersin?

## Mini alıştırma
%0.2 error ve %1 slow request olan servis için error/slow trace'leri yüksek oranda koruyan, normal trace'leri %5'e indiren policy tasarla. Sampler memory, dropped spans ve per-policy sampled count ile doğrula.

## Kaynaklar
- https://opentelemetry.io/docs/concepts/sampling/
- https://opentelemetry.io/docs/collector/
- https://opentelemetry.io/docs/collector/components/processor/
- https://opentelemetry.io/docs/demo/sample-configurations/
