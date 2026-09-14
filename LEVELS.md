# Engineering Levels Matrix

Bu belge, aynı teknik konunun **Junior'dan CTO'ya kadar hangi derinlikte bilinmesi gerektiğini** tarif eder. Amaç ezber listesi çıkarmak değil; teknik derinlik, karar kalitesi, etki alanı ve liderlik beklentisini netleştirmektir.

> Not: Şirketler seviye isimlerini farklı kullanabilir. Buradaki çerçeve genel bir referanstır.

## Seviye özeti

| Seviye | Ana odak | Tipik kapsam | Mülakatta beklenen düşünme biçimi |
|---|---|---|---|
| Junior | Temeller ve doğru uygulama | Tek görev / küçük modül | Kavramı doğru tanımlar, basit örnek çözer |
| Mid | Bağımsız uygulama ve debugging | Servis / feature | Trade-off'ları fark eder, üretim hatalarını teşhis eder |
| Senior | Sistem sahipliği | Birkaç servis / kritik akış | Failure mode, performans, güvenlik ve operasyon düşünür |
| Staff | Çoklu ekip teknik yön | Domain / platform | Organizasyon çapında trade-off, blast radius, standartlaşma |
| Principal | Şirket ölçeğinde teknik strateji | Birden fazla domain | Uzun vadeli mimari, teknoloji yönü, platform stratejisi |
| Engineering Manager | İnsan + teslimat + teknik risk | Takım / takımlar | Öncelik, kapasite, hiring, risk ve execution |
| CTO | İş + teknoloji stratejisi | Şirket | Maliyet, rekabet avantajı, organizasyon, risk ve zamanlama |

## Teknik derinlik matrisi

### Algorithms & Data Structures
- **Junior:** Big-O, array, hash map, stack, queue, linked list, tree, BFS/DFS.
- **Mid:** Problem pattern'leri, heap, interval, sliding window, binary search varyasyonları.
- **Senior:** Algoritma seçimini gerçek sistem kısıtlarıyla ilişkilendirir; memory/latency trade-off'larını açıklar.
- **Staff/Principal:** Algoritmik kararların platform maliyetine etkisini değerlendirir; gerektiğinde özel veri yapıları tasarlar.
- **EM/CTO:** Her ayrıntıyı kodlaması gerekmez; ekipte doğru teknik bar ve değerlendirme standardını kurar.

### Backend & APIs
- **Junior:** HTTP, REST, status code, validation, CRUD, authentication temelleri.
- **Mid:** Pagination, idempotency, caching, retries, queues, API versioning.
- **Senior:** Backpressure, rate limiting, graceful degradation, observability, security boundaries.
- **Staff:** API governance, platform abstractions, multi-tenancy, cross-team standards.
- **Principal:** Şirket çapında servis mimarisi ve platform stratejisi.
- **EM/CTO:** Build-vs-buy, organizasyon kapasitesi, platform yatırımının geri dönüşü.

### Databases
- **Junior:** SQL, index, primary key, transaction temelleri.
- **Mid:** Query plans, isolation levels, normalization, replication temelleri.
- **Senior:** Locking, hot partitions, sharding, migration, connection pools, failure recovery.
- **Staff:** Multi-region veri mimarisi, data ownership, schema evolution, tenancy.
- **Principal:** Storage platform stratejisi, consistency modelleri ve uzun vadeli maliyet.
- **EM/CTO:** Veri regülasyonu, vendor riski, operasyon maliyeti ve ölçek ekonomisi.

### Distributed Systems
- **Junior:** Client/server, latency, retry, timeout kavramları.
- **Mid:** Replication, partitioning, message queues, eventual consistency.
- **Senior:** Idempotency, consensus temelleri, retries/storms, ordering, CDC, failure domains.
- **Staff:** Multi-region, control plane/data plane, blast radius, overload protection, platform design.
- **Principal:** Şirket ölçeğinde reliability/consistency stratejisi ve mimari sadeleştirme.
- **EM/CTO:** Reliability hedeflerini iş etkisi ve maliyetle dengeler.

### Cloud / DevOps / SRE
- **Junior:** Containers, CI/CD, temel cloud servisleri.
- **Mid:** Kubernetes primitives, monitoring, deployment strategies.
- **Senior:** SLO/SLI, incident response, capacity, autoscaling, probes, rollout safety.
- **Staff:** Reliability platformu, shared infrastructure, operational maturity.
- **Principal:** Multi-region/cloud strategy, resilience standards, platform economics.
- **EM/CTO:** Cloud maliyeti, vendor lock-in, reliability yatırımı ve ekip yapısı.

### Cybersecurity
- **Junior:** Authentication vs authorization, OWASP temel riskleri, secrets.
- **Mid:** OAuth/OIDC, RBAC, secure coding, threat basics.
- **Senior:** Threat modeling, service identity, Zero Trust, tenant isolation, auditability.
- **Staff:** Security architecture, policy enforcement, blast radius reduction.
- **Principal:** Şirket çapında trust model ve security platform stratejisi.
- **EM/CTO:** Risk iştahı, compliance, güvenlik yatırımı ve incident governance.

### Data Engineering
- **Junior:** ETL/ELT, SQL, batch vs stream.
- **Mid:** Kafka, partitioning, data warehouse/lake, orchestration.
- **Senior:** CDC, schema evolution, exactly-once vs at-least-once, data quality.
- **Staff:** Data platform, governance, lineage, cost/performance.
- **Principal:** Kurumsal veri mimarisi ve self-service platform stratejisi.
- **EM/CTO:** Veri organizasyonu, ownership modeli, platform ROI.

### AI / ML / LLM
- **Junior:** Train/validation/test, overfitting, temel model kavramları.
- **Mid:** Embeddings, transformers temelleri, evaluation, RAG.
- **Senior:** Serving, latency/cost, eval pipelines, safety, retrieval quality.
- **Staff:** AI platform, model gateway, observability, data flywheel, multi-model strategy.
- **Principal:** Şirket ölçeğinde AI architecture ve platform direction.
- **EM/CTO:** AI'nin gerçek iş değeri, risk, maliyet, moat ve build-vs-buy kararları.

### Networking
- **Junior:** TCP/IP, DNS, HTTP, TLS temel akışı.
- **Mid:** Load balancer, NAT, connection lifecycle, keep-alive.
- **Senior:** Tail latency, connection exhaustion, retries, packet loss etkileri.
- **Staff:** Service networking, ingress/egress, multi-region traffic architecture.
- **Principal:** Şirket çapında network/platform strategy.
- **EM/CTO:** Network maliyeti, güvenlik ve global expansion trade-off'ları.

## Aynı soruya seviyeye göre cevap örneği

**Soru:** "Cache neden kullanılır?"

- **Junior:** Database'e gitmeden daha hızlı veri döndürmek için.
- **Mid:** Latency ve DB yükünü azaltır; TTL, cache miss ve invalidation konuşur.
- **Senior:** Stampede, stale data, consistency, eviction, failure behavior ve observability ekler.
- **Staff:** Shared cache platformu, tenancy, regional cache, blast radius ve ownership modelini tartışır.
- **Principal:** Cache'in bütün platform mimarisindeki rolünü ve uzun vadeli standartları belirler.
- **EM:** Ekibin cache kullanımını güvenli ve sürdürülebilir hale getirecek süreç/ownership kurar.
- **CTO:** Cache yatırımının infra maliyeti, ürün latency'si ve ekip karmaşıklığı üzerindeki etkisini değerlendirir.

## Mülakat hazırlığında kullanım

Her konu çalışılırken şu dört soruya cevap ver:

1. **Tanım:** Bu nedir?
2. **Mekanizma:** İçeride nasıl çalışır?
3. **Failure:** Bozulduğunda ne olur?
4. **Trade-off:** Hangi durumda başka bir çözüm seçerdim?

Seviye yükseldikçe beşinci soru eklenir:

5. **Organizasyon ve iş etkisi:** Bu karar ekipleri, maliyeti, güvenliği ve ürün stratejisini nasıl etkiler?
