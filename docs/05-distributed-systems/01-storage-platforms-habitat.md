# Storage Platformları: Habitat Üzerinden Distributed Systems Okumak

Bu bölüm, OpenAI'nin yayımladığı Habitat storage platformu diyagramını bir “system design dersliği” olarak kullanır. Amaç tek bir şirketin mimarisini ezberlemek değil; büyük ölçekli storage platformlarında tekrar eden fikirleri öğrenmektir.

## 1. Problem ne?

Büyük bir organizasyonda her ürün ekibinin ayrı ayrı şu problemleri çözmesi pahalıdır:

- hangi database/storage kullanılacak?
- request hangi shard/region'a gidecek?
- authorization nerede uygulanacak?
- cache nasıl kullanılacak?
- connection pooling nasıl yapılacak?
- rate limit / overload protection nasıl uygulanacak?
- tenant'lar nasıl izole edilecek?
- veri hangi coğrafyada tutulacak?
- database değişiklikleri analytics/search sistemlerine nasıl aktarılacak?

Bu problemlerin ortak bir platformda toplanması bir **storage abstraction layer / storage platform** yaklaşımıdır.

## 2. Basit mental model

```text
Products / Services
        ↓
┌─────────────────────────┐
│   Storage Platform      │
│ auth • routing • cache  │
│ policy • rate limiting  │
└─────────────────────────┘
    ↓        ↓        ↓
Online DB   Cache    Blob/Object
    ↓
   CDC
    ↓
Analytics / Search / Streams
```

Burada storage platformunun değeri yalnızca “database proxy” olmak değildir. Cross-cutting concern'leri merkezi hale getirir.

## 3. Abstraction'ın avantajı

Product developer şunu düşünmek ister:

```text
get(user_id)
put(user_id, value)
```

Şunları her feature için yeniden düşünmek istemez:

```text
hangi region?
hangi shard?
hangi credential?
hangi retry policy?
hangi serializer?
hangi connection pool?
```

İyi abstraction cognitive load'u azaltır ve organizasyon çapında standardizasyon sağlar.

## 4. Ama abstraction bedava değildir

Staff/Principal mülakatının kritik noktası burada başlar.

Merkezi platform:

- büyük blast radius yaratabilir,
- ekstra network hop ekleyebilir,
- yanlış abstraction ile product ekiplerini kısıtlayabilir,
- merkezi ekibi bottleneck'e çevirebilir,
- migration'ları zorlaştırabilir.

Bu yüzden soru “platform yapalım mı?” değil:

> Hangi problemlerin merkezi çözümü toplam sistem karmaşıklığını gerçekten azaltıyor?

## 5. Routing

Routing katmanı bir request'in hangi backend'e ulaşacağını belirler.

Örnek:

```text
request(user=42)
      ↓
metadata/schema lookup
      ↓
region / shard / backend seçimi
      ↓
DB shard 17
```

Routing kararı şu bilgilere bağlı olabilir:

- tenant
- data residency
- partition key
- schema/version
- capacity
- failover state

### Mülakat sorusu

**“Routing metadata servisi down olursa ne olur?”**

Senior cevap: cache, timeout ve failure handling konuşur.

Staff cevap: control plane / data plane ayrımı, stale-but-safe metadata, blast radius ve failover davranışını da konuşur.

## 6. Authorization ve tenant isolation

Authentication:

> Sen kimsin?

Authorization:

> Bu kaynağa bu işlemi yapabilir misin?

Multi-tenant storage'da her request için tenant identity'nin doğru taşınması kritik olabilir.

Kötü örnek:

```sql
SELECT * FROM orders WHERE order_id = ?;
```

Daha güvenli modelin bir parçası:

```sql
SELECT * FROM orders
WHERE tenant_id = ? AND order_id = ?;
```

Fakat yalnızca SQL filtresi security architecture değildir. Service identity, policy enforcement, audit, encryption ve least privilege birlikte düşünülmelidir.

## 7. Cache

```text
Client
  ↓
Storage layer
  ↓
Cache ─ hit → response
  ↓ miss
Database
```

Cache latency ve database load'u düşürür ama yeni problemler getirir:

- invalidation
- stale data
- eviction
- cache stampede
- hot keys
- consistency

### Interview follow-up

“Bir hot key milyonlarca request alırsa?”

Beklenebilecek fikirler:

- local caching
- request coalescing
- replication
- TTL jitter
- sharding (mümkünse)
- load shedding

## 8. Rate limiting ve overload protection

Rate limiting yalnızca kötü niyetli client'ları durdurmak için değildir; sistemin dependency'lerini korumak için de kullanılır.

```text
Incoming traffic
      ↓
Rate limiter
      ↓
Bounded concurrency
      ↓
Storage
```

Staff seviyesinde şu kavramları birlikte düşün:

- rate limit
- concurrency limit
- queue bound
- timeout
- retry budget
- backpressure
- load shedding

Sınırsız queue çoğu zaman kapasite değildir; sadece failure'ı geciktirir.

## 9. Data residency

Bazı verilerin belirli coğrafyalarda tutulması gerekebilir. Routing ve placement policy'leri buna göre çalışabilir.

Bu konu yalnızca compliance değildir:

- latency
- disaster recovery
- operational ownership
- encryption key placement
- cross-region transfer cost

gibi faktörlere de dokunur.

## 10. Online storage ile analytics'i ayırmak

Production request path'i çoğunlukla düşük ve öngörülebilir latency ister. Analytics sorguları ise büyük scan/join/aggregation yapabilir.

Bu yüzden tipik pattern:

```text
Application
    ↓
Online DB
    ↓
CDC
    ↓
Kafka / stream
    ↓
Search / Analytics / Warehouse
```

Bu separation of workloads, online DB'nin ağır analytical query'lerden korunmasına yardımcı olur.

## 11. CDC

Change Data Capture, database'deki değişiklikleri downstream sistemlere event/record olarak taşımak için kullanılan yaklaşımdır.

```text
user.plan = free → pro

        ↓ CDC

{ user_id: 42, old: free, new: pro }
```

Zor sorular:

- duplicate event?
- ordering?
- schema evolution?
- consumer lag?
- replay?
- poison event?
- exactly-once gerçekten gerekli mi?

Bu sorular Senior/Staff interview'lerinde teknolojinin adından daha değerlidir.

## 12. Seviyelere göre mülakat soruları

### Junior
1. Cache ne işe yarar?
2. Authentication ve authorization farkı nedir?
3. Blob/object storage ile database farkı nedir?
4. Rate limiting nedir?
5. Database replica nedir?

### Mid
1. Cache invalidation nasıl yapılır?
2. Connection pooling neden gerekir?
3. Partition key nasıl seçilir?
4. Retry ne zaman tehlikelidir?
5. CDC ne işe yarar?

### Senior
1. Hot partition nasıl oluşur?
2. Retry storm'u nasıl engellersin?
3. Multi-tenant isolation nasıl tasarlanır?
4. Tail latency nasıl azaltılır?
5. Online ve analytical workload'u nasıl ayırırsın?

### Staff / Principal
1. Storage abstraction'ın sınırlarını nasıl belirlersin?
2. Merkezi platformun blast radius'unu nasıl azaltırsın?
3. Control plane down olduğunda data plane çalışmaya devam edebilir mi?
4. Multi-region consistency modelini nasıl seçersin?
5. Platform adoption'ını zorlamadan standardizasyonu nasıl sağlarsın?
6. Migration'ı müşterilere görünmez nasıl yaparsın?

### Engineering Manager
1. Platform takımının roadmap'i product ekipleriyle nasıl dengelenir?
2. Reliability work'ünün değerini nasıl ölçersin?
3. Platform ownership sınırı nerede olmalı?
4. Incident sonrası hangi action item'ların gerçekten yapılacağını nasıl sağlarsın?

### CTO
1. Kendi storage platformunu yapmak mı managed service kullanmak mı?
2. Vendor concentration risk'i nasıl değerlendirilir?
3. Multi-cloud gerçekten gerekli mi?
4. Data residency şirket stratejisini nasıl etkiler?
5. Platform yatırımı ne zaman organization leverage üretir?

## 13. 30 dakikalık uygulama

“10 milyon tenant'lı SaaS storage gateway” tasarla.

Requirement:

```text
GET /v1/objects/{id}
PUT /v1/objects/{id}
```

Şunları çiz:

1. API gateway
2. authn/authz
3. tenant routing
4. cache
5. storage backend
6. rate/concurrency limiting
7. logs/metrics/tracing
8. CDC output

Sonra şu failure'ları tek tek uygula:

- cache down
- DB shard down
- routing metadata stale
- region down
- bir tenant 100x trafik gönderiyor

Her durumda:

```text
Ne bozulur?
Blast radius ne?
Fail-open / fail-closed?
Recovery nasıl?
```

sorularını cevapla.

## 14. Portföy projesi

### `mini-storage-gateway`

Örnek kapsam:

```text
client
  ↓
FastAPI/Go API
  ↓
JWT/API-key auth
  ↓
rate limiter
  ↓
Redis/Valkey cache
  ↓
PostgreSQL
  ↓
outbox/CDC simulation
  ↓
Kafka/Redpanda
```

Ekstra puan:

- OpenTelemetry traces
- p95/p99 latency dashboard
- load test
- chaos test
- idempotency key
- tenant quota
- architecture decision records

Bu proje backend + distributed systems + DevOps + observability + security konuşabilmek için tek repo içinde güçlü bir örnek olur.

## 15. Birincil / güçlü kaynaklar

- OpenAI — Rapidly scaling online storage to serve over 1 billion ChatGPT users: https://openai.com/index/scaling-storage-one-billion-users-part-one/
- Azure Cosmos DB overview: https://learn.microsoft.com/azure/cosmos-db/overview
- Valkey documentation: https://valkey.io/topics/introduction/
- Apache Kafka documentation: https://kafka.apache.org/documentation/
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- NIST Zero Trust Architecture (SP 800-207): https://csrc.nist.gov/pubs/sp/800/207/final

## 16. Görsel kaynağı notu

OpenAI'nin Habitat mimari görseli yukarıdaki OpenAI engineering yazısında yer alır. Telifli kaynağı repoya kopyalamak yerine resmi yazıya bağlantı verilir; bu repodaki şemalar ise özgün eğitim diyagramları olarak tutulacaktır.
