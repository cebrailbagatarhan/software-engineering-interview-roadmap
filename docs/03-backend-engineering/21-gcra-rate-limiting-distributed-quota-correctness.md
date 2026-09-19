# GCRA Rate Limiting: Virtual Scheduling & Distributed Quota Correctness

**Seviye:** Mid → Principal  
**Alan:** Backend / Distributed Systems

## Konu anlatımı
Generic Cell Rate Algorithm (GCRA), rate limiting’i request geçmişi listesi yerine theoretical arrival time (TAT) ile modeller. Kabul edilen request TAT’i emission interval kadar ileri iter; request burst tolerance hesaba katıldıktan sonra fazla erken gelirse reddedilir. Böylece tek zaman state’iyle smooth pacing, burst ve `Retry-After` üretilebilir.

## Mental model
```text
real time ---- now ---------------------------->
TAT --------------------- next ideal slot ----->
       <--- burst tolerance --->

allow  => TAT = max(TAT, now) + cost * interval
reject => state değişmez
```
**Invariant:** Aynı quota key’i için admission kararı ile TAT update’i atomik olmalıdır.

## İçeride ne oluyor?
- `interval = period / rate`; weighted cost TAT’i `cost * interval` ilerletir.
- Burst tolerance kısa kümelenmeye izin verir, uzun dönem rate’i değiştirmez.
- Redis + atomic script/module global coordination sağlayabilir fakat network latency ekler.
- Replica-local limiter hızlıdır fakat strict global quota sağlamaz.
- Credit leasing store QPS’yi azaltır; bounded overshoot gerektirir.
- Clock jumps ve unit conversion hataları fairness/correctness’i bozar.

## Mülakat soruları
1. Fixed-window boundary burst nedir?
2. Token bucket ile GCRA’yı karşılaştır.
3. GCRA neden tek timestamp state’iyle çalışabilir?
4. Retry-after nasıl türetilir?
5. Local limiter global quota’yı neden garanti etmez?
6. Senior: Redis outage’ında fail-open/fail-closed kararı?
7. Staff: tenant/user/endpoint hierarchical quota nasıl tasarlanır?
8. Principal: strictness, availability, latency ve revenue protection nasıl dengelenir?

## Beklenen cevap seviyesi
- **Mid:** rate/burst/TAT/retry semantics’i açıklar.
- **Senior:** atomicity, clock, outage ve hot-key problemlerini çözer.
- **Staff:** sharding, multi-dimensional quota, leasing ve telemetry tasarlar.
- **Principal:** correctness seviyesini SLO, abuse ve ürün ekonomisine bağlar.

## Mini alıştırma
10 req/s ve burst=5 için 12 arrival timestamp üzerinde allow/reject, TAT ve retry-after hesapla; fixed-window sonucu ile karşılaştır.

## Proje fikri
`gcra-distributed-limiter-lab`: üç API replica + Redis atomic GCRA kur. Store latency/partition enjekte edip strict, fail-open ve local-credit modlarında overshoot, p99 ve availability ölç.

## Failure modes / trade-off / production
Non-atomic GET/SET overshoot, hot-key hotspot, clock/unit bug unfair throttling, unbounded key cardinality memory blow-up, fail-open abuse ve fail-closed outage amplification yaratır. Production’da allow/deny, retry-after, store p99, hot-key distribution, limiter errors, overshoot ve config version izlenir.

## Kaynaklar
- `redis-cell` — GCRA Redis module ve `CL.THROTTLE`: https://github.com/brandur/redis-cell
- `go-redis/redis_rate` — Redis-backed GCRA implementation: https://github.com/go-redis/redis_rate
