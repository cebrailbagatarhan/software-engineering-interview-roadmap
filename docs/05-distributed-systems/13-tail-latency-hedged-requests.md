# Tail Latency & Hedged Requests

## Problem
Fan-out sistemlerde aggregate latency çoğu zaman en yavaş alt isteğe bağlıdır. Küçük bir per-node straggler olasılığı yüzlerce paralel alt istekte kullanıcıların önemli bölümünü etkileyebilir.

```text
client -> aggregator -> R1
                   \-> R2
                   \-> R3 (straggler)

hedge:
primary -> A ---- slow ----X
       \-> B after delay -> WIN
```

## Mental model
Hedging failure sonrası retry değildir; **henüz bitmemiş yavaş isteğe karşı spekülatif ikinci execution**'dır. İlk başarılı cevap kazanır, kalan istek iptal edilir. Tail düşebilir fakat ekstra work oluşur.

## Fan-out etkisi
Her shard'ın slow olma olasılığı `p`, bağımsız shard sayısı `n` ise en az bir slow shard olasılığı yaklaşık `1-(1-p)^n` olur. Bu yüzden ortalama latency tek başına distributed user experience'i temsil etmez.

## Güvenli hedging prensipleri
- Öncelikle idempotent/read operasyonlarda kullan.
- Hedge delay'i workload percentile'larından türet; sıfır-delay duplicate work'ü büyütür.
- Global deadline tüm attempts'i sınırlandırmalıdır.
- Cancellation'ın backend execution'ı anında durduracağını varsayma.
- Saturation sırasında hedge storm'u engellemek için throttling/pushback gerekir.
- Replica'lar aynı correlated failure domain'indeyse fayda azalır.

## gRPC bağlantısı
gRPC request hedging per-method `maxAttempts`, `hedgingDelay`, `nonFatalStatusCodes` ve retry throttling yapılandırmaları sunar. İlk başarılı cevap sonrası outstanding hedges cancel edilir; server pushback yeni hedge'leri geciktirebilir veya durdurabilir.

## Seviye beklentisi
Junior percentile/timeout; Mid fan-out ve retry-vs-hedge; Senior idempotency, cancellation ve load amplification; Staff adaptive throttling, headroom ve SLO; Principal/CTO overprovisioning ile software complexity ekonomisini açıklamalıdır.

## Production metrikleri
Hedge rate, winning-secondary rate, request amplification, cancellation latency, per-replica queue depth/utilization, p95/p99/p999 ve overload state.

## Kaynaklar
- https://research.google/pubs/the-tail-at-scale/
- https://barroso.org/publications/TheTailAtScale.pdf
- https://grpc.io/docs/guides/request-hedging/
