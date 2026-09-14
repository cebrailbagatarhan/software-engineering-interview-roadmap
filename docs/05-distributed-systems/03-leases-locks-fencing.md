# Leases, Distributed Locks ve Fencing Tokens

Distributed coordination'da kritik soru yalnızca "lock var mı?" değildir; bir actor'ın hâlâ yetkili olup olmadığını downstream sistemin nasıl anlayacağıdır.

## Lease mental modeli
Bir lease zaman sınırlı ownership'tir. Owner lease'i yeniler. Renewal kesilirse başka candidate sahipliği alabilir. Kubernetes Lease nesnelerini node heartbeat ve leader election gibi coordination görevlerinde kullanır.

```mermaid
sequenceDiagram
  participant A as Owner A
  participant C as Coordinator
  participant B as Owner B
  participant S as Storage
  A->>C: acquire -> epoch 10
  A->>S: mutate(epoch=10)
  Note over A: pause / partition
  B->>C: lease expired; acquire -> epoch 11
  B->>S: mutate(epoch=11)
  A->>S: late mutate(epoch=10)
  S-->>A: reject stale epoch
```

## Neden TTL yetmez?
Bir process lease süresinden uzun süre pause olabilir ve daha sonra kaldığı yerden devam edebilir. O sırada başka owner lease'i almış olabilir. Eski process yalnızca local olarak "ben lock sahibiydim" bilgisine güvenirse stale write yapabilir.

## Fencing token
Her başarılı ownership devri monoton artan token/epoch üretir. Protected resource gördüğü en yüksek epoch'u hatırlar ve daha düşük epoch'lu operation'ı reddeder. Böylece authorization yalnız coordinator'da değil, mutation'ın gerçekleştiği boundary'de enforce edilir.

## Mülakat soruları
- Lease ile mutex arasındaki fark nedir?
- GC pause veya network partition eski owner'ı nasıl tehlikeli yapar?
- Fencing token neden monoton olmalıdır?
- Token nerede validate edilmelidir?
- Idempotency distributed lock ihtiyacını ne zaman azaltır?
- Safety ve availability arasında nasıl seçim yaparsın?

## Production trade-off'ları
Strong coordination latency ve availability maliyeti getirir. Duplicate work tolere edilebiliyorsa idempotent operations, partitioned ownership veya compare-and-swap daha basit olabilir. Correctness kritik metadata mutation, storage attachment ve migration ownership gibi alanlarda stale-owner riskini açıkça modellemek gerekir.

Habitat-benzeri storage platformunda adapter leadership, volume ownership veya migration coordinator lease ile seçilebilir; backend mutation fencing epoch ile korunabilir.

## Kaynaklar
- Redis Distributed Locks: https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/
- Kubernetes Leases: https://kubernetes.io/docs/concepts/architecture/leases/
- Kubernetes Lease API: https://kubernetes.io/docs/reference/kubernetes-api/coordination/lease-v1/
