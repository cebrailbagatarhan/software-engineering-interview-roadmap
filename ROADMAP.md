# Software Engineering Interview Roadmap

Bu roadmap, konuları rastgele ezberlemek yerine **temelden üretim sistemlerine** doğru ilerlemek için tasarlanmıştır. Hedef yalnızca mülakat geçmek değil; soruların arkasındaki mühendislik mantığını kurabilmektir.

## Nasıl çalışılmalı?

Her konu için şu döngüyü uygula:

```text
Öğren → Çiz → Açıkla → Kodla → Boz → Ölç → Mülakat sorusu çöz → Gerçek sisteme bağla
```

Bir konuyu gerçekten öğrendiğini şu durumda kabul et:

- Basitçe tanımlayabiliyorsun.
- Bir diyagramla açıklayabiliyorsun.
- Çalışma mantığını anlatabiliyorsun.
- Failure mode'larını sayabiliyorsun.
- Trade-off'larını tartışabiliyorsun.
- Küçük bir implementasyon yapabiliyorsun.
- Junior ve Senior cevabı arasındaki farkı gösterebiliyorsun.

---

## Aşama 1 — Computer Systems Foundations

Önce bilgisayarın altında ne olduğunu anlamak gerekir.

### Konular
- CPU, instruction cycle, pipeline
- Register, cache, RAM, memory hierarchy
- Process vs thread
- Context switch
- Virtual memory
- Stack vs heap
- Concurrency ve synchronization
- File systems
- Syscalls

### Yapılabilir projeler
- Mini thread pool
- Producer/consumer queue
- Basit memory allocator simülasyonu
- LRU cache

### Mülakat çıktısı
Junior/Mid için fundamentals; Senior için latency, contention, memory ve concurrency reasoning.

---

## Aşama 2 — Algorithms & Data Structures

### Temel veri yapıları
- Array / string
- Hash map / set
- Stack / queue
- Linked list
- Tree / BST
- Heap
- Graph
- Trie

### Problem pattern'leri
- Two pointers
- Sliding window
- Binary search
- Prefix sum
- BFS / DFS
- Backtracking
- Dynamic programming
- Greedy
- Intervals
- Topological sort

### Hedef
Sadece çözmek değil, çözümün neden `O(n)` veya `O(n log n)` olduğunu açıklamak.

---

## Aşama 3 — Networking

### Konular
- OSI ve TCP/IP modeli
- IP, subnet, routing
- TCP vs UDP
- TCP handshake
- DNS
- HTTP/1.1, HTTP/2, HTTP/3
- TLS
- Load balancers
- CDN
- NAT
- Connection pooling / keep-alive

### Proje
HTTP server + reverse proxy + basit load balancer yaz.

### Senior sorusu
"Bir request neden bazen 50 ms, bazen 2 saniye sürer?"

Buradan tail latency, packet loss, retries, DNS, connection setup ve downstream dependency analizine git.

---

## Aşama 4 — Backend Engineering

### Konular
- REST / RPC / gRPC
- API design
- Pagination
- Idempotency
- Authentication / authorization
- Rate limiting
- Caching
- Background jobs
- Queues
- Retries / timeout / circuit breaker
- Backpressure
- API versioning

### Portföy projeleri
- Token bucket rate limiter
- URL shortener API
- Job queue
- API gateway

---

## Aşama 5 — Databases

### Relational
- SQL
- Index
- B-tree
- Transactions
- ACID
- Isolation levels
- Locks / MVCC
- Query planner

### Distributed storage
- Replication
- Sharding
- Partition key
- Hot partitions
- Read/write replicas
- Consistency
- Schema evolution
- Online migrations

### NoSQL ve storage engines
- Key-value
- Document
- Column-family
- LSM tree
- WAL
- Compaction

### Proje
Basit persistent key-value store oluştur.

---

## Aşama 6 — Distributed Systems

Bu bölüm Senior+ seviyelerde kritik hale gelir.

### Konular
- Partial failure
- Timeout/retry
- Idempotency
- Replication
- Partitioning
- Consistency models
- CAP ve PACELC
- Leader election
- Consensus / Raft temelleri
- Logical clocks
- Distributed locks
- Queues / streams
- CDC
- Event-driven architecture
- Backpressure
- Load shedding
- Multi-region systems

### Case study
OpenAI Habitat benzeri bir storage platformunu parçala:

```text
Clients
   ↓
Storage platform
   ├─ auth
   ├─ routing
   ├─ rate limiting
   ├─ tenancy
   ├─ caching
   └─ residency
   ↓
Storage backends
   ↓
CDC → analytics/search/streaming
```

Her kutu için sor:

1. Neden var?
2. Bozulursa ne olur?
3. Blast radius nedir?
4. Hangi metric izlenir?
5. Alternatifi nedir?

---

## Aşama 7 — System Design

Klasik soruları ezberlemek yerine reusable building block'ları öğren.

### Design soruları
- URL shortener
- Chat system
- Notification service
- News feed
- File storage
- Video streaming
- Payment system
- Search autocomplete
- Metrics platform
- Distributed cache
- Job scheduler
- API rate limiter
- Multi-tenant storage platform

### Her tasarımda standart sıra

```text
Requirements
→ Scale estimation
→ API
→ Data model
→ High-level architecture
→ Bottlenecks
→ Consistency
→ Failure modes
→ Security
→ Observability
→ Cost
→ Trade-offs
```

---

## Aşama 8 — Cloud, DevOps & SRE

### Konular
- Containers
- Docker
- Kubernetes
- CI/CD
- Infrastructure as Code
- Autoscaling
- Service discovery
- Health probes
- Observability
- Metrics/logs/traces
- SLI/SLO/SLA
- Error budgets
- Incident response
- Capacity planning
- Multi-region deployment
- Disaster recovery

### Proje
Kubernetes üzerinde deploy edilen, metrics + tracing + alerts içeren küçük production-like servis.

---

## Aşama 9 — Cybersecurity

### Konular
- Authentication vs authorization
- OAuth 2.0
- OpenID Connect
- JWT
- Session security
- RBAC / ABAC
- OWASP API Security
- SQL injection / XSS / CSRF
- Secrets management
- TLS
- Zero Trust
- Threat modeling
- Service identity
- Least privilege
- Tenant isolation
- Audit logs

### Proje
OAuth/OIDC tabanlı multi-role API + threat model dokümanı.

---

## Aşama 10 — Data Engineering

### Konular
- ETL / ELT
- Batch vs streaming
- Kafka
- Topics / partitions / consumer groups
- CDC
- Data lake / warehouse / lakehouse
- Schema evolution
- Data quality
- Orchestration
- Lineage
- OLTP vs OLAP

### Proje
Database → CDC → Kafka → analytics store pipeline.

---

## Aşama 11 — AI / ML / LLM

### ML fundamentals
- Train / validation / test
- Bias / variance
- Overfitting
- Metrics
- Feature engineering

### Deep learning
- Neural networks
- Backpropagation
- Embeddings
- Attention
- Transformer

### LLM systems
- Tokenization
- Context window
- Prompting
- Embeddings
- Vector search
- RAG
- Evaluation
- Guardrails
- Agent systems
- Inference latency / throughput

### Proje
RAG uygulaması + offline/online evaluation pipeline.

---

## Aşama 12 — MLOps / AI Infrastructure

### Konular
- Model serving
- Batch vs online inference
- GPU utilization
- Batching
- Model registry
- Feature store
- Experiment tracking
- Model/data drift
- LLM observability
- Eval pipelines
- Rollbacks / canary releases
- Cost per request/token

### Staff sorusu
"10 farklı model kullanan şirket için merkezi AI gateway nasıl tasarlanır?"

---

## Aşama 13 — Frontend / Mobile

### Konular
- Browser rendering pipeline
- DOM / event loop
- State management
- Network performance
- Caching
- Web security
- Accessibility
- Mobile lifecycle
- Offline-first
- Push notifications
- App performance

---

## Aşama 14 — Staff / Principal Engineering

Burada teknoloji bilgisinin yanında **etki alanı** değişir.

### Beklentiler
- Cross-team architecture
- Platform thinking
- Technical strategy
- Migration planning
- Technical debt management
- Reliability standards
- Architecture reviews
- Mentoring
- Decision records
- Build vs buy
- Organizational constraints

### Çalışma soruları
- 30 takımlı şirkette ortak authentication nasıl standartlaştırılır?
- Monolith'i gerçekten parçalamak gerekli mi?
- Bir platform ekibi ne zaman kurulmalı?
- Global outage blast radius'u nasıl küçültülür?

---

## Aşama 15 — Engineering Management & CTO

### Engineering Manager
- Hiring
- Performance management
- Delivery
- Team topology
- Planning
- Incident leadership
- Technical debt prioritization
- Stakeholder communication

### CTO
- Technical strategy
- Architecture governance
- Build vs buy
- Cloud / vendor economics
- Security & compliance
- Hiring strategy
- Engineering productivity
- AI strategy
- Platform investments
- Risk management

### CTO seviyesinde temel soru

> "Teknik olarak yapılabiliyor" ile "şirket için yapılmalı" arasındaki fark nedir?

---

# Önerilen çalışma sırası

```text
CPU / OS
   ↓
Algorithms
   ↓
Networking
   ↓
Backend
   ↓
Databases
   ↓
Distributed Systems
   ↓
System Design
   ↓
Cloud / SRE
   ↓
Security
   ↓
Data Engineering
   ↓
AI / ML / LLM
   ↓
MLOps
   ↓
Staff / Principal
   ↓
EM / CTO
```

Bu sıra katı değildir. Mülakat hedefi ve rol tipine göre paralel çalışılabilir.

## Repo çalışma modeli

- `daily/` → saatlik ham çalışma paketleri
- `docs/` → temizlenmiş, kalıcı kitap bölümleri
- `questions/` → seviye bazlı soru bankası
- `labs/` → uygulama projeleri
- `system-design/` → uçtan uca tasarım vakaları
- `assets/` → özgün diyagram ve görseller
- `references/` → güvenilir kaynak dizini

Amaç zamanla bu repoyu **Türkçe Software Engineering Interview & Systems Handbook** haline getirmektir.
