# Software Engineering Interview Roadmap

Bu repo, **Junior → Mid → Senior → Staff → Principal → Engineering Manager → CTO** seviyelerinde yazılım mülakatlarına hazırlanmak için yaşayan bir Türkçe mühendislik kitabı ve çalışma deposudur.

Amaç yalnızca soru ezberlemek değil; bir konuyu **temelden öğrenmek → sistem içinde nasıl çalıştığını anlamak → mülakatta açıklayabilmek → küçük bir uygulama ile pekiştirmek → daha üst seviyedeki trade-off'ları tartışabilmek**.

> Not: İçerik, herhangi bir yazarın üslubunu birebir taklit etmez. Ders kitabı gibi katmanlı, sezgisel, bol örnekli ve teknik derinliği giderek artan bir anlatım hedefler.

## Nasıl kullanılmalı?

Her bölüm mümkün olduğunca şu şablonu izler:

1. **Konu anlatımı** — kavramın ne olduğu ve neden var olduğu
2. **Mental model** — akılda kalıcı basit model
3. **İçeride ne oluyor?** — implementation / internals
4. **Mülakat soruları** — seviyeye göre Junior'dan Staff/CTO'ya
5. **Beklenen cevap seviyesi** — interviewer ne duymak ister?
6. **Mini alıştırma** — 10–30 dakikalık uygulama
7. **Proje fikri** — portföye dönüşebilecek örnek
8. **Production bağlantısı** — gerçek sistemlerde nerede kullanılır?
9. **Kaynaklar** — mümkün olduğunca resmi dokümantasyon / birincil kaynak
10. **Görseller** — özgün SVG/Mermaid diyagramları ve gerektiğinde resmi kaynak görsellerine bağlantılar

## Kitap / Roadmap

### Bölüm I — Computer Science Foundations
- CPU: instruction cycle, registers, cache, branch prediction
- Memory hierarchy: registers → cache → RAM → disk
- Processes, threads, context switching
- Virtual memory, paging, page faults
- Filesystems
- Concurrency, synchronization, deadlocks
- Networking foundations: TCP/IP, DNS, HTTP/TLS

### Bölüm II — Algorithms & Data Structures
- Big-O ve amortized analysis
- Arrays, strings, hash tables
- Linked lists, stacks, queues
- Trees, heaps, tries
- Graphs, BFS/DFS, shortest path
- Sorting/searching
- Dynamic programming
- Greedy algorithms
- Interview patterns: two pointers, sliding window, binary search, prefix sums

### Bölüm III — Backend Engineering
- HTTP/API design
- REST, RPC, gRPC
- Authentication vs authorization
- Caching
- Rate limiting
- Queues
- Background jobs
- Idempotency
- Observability

### Bölüm IV — Databases
- Relational model ve SQL
- Indexes / B+Tree
- Transactions ve ACID
- Isolation levels / MVCC
- Query planning
- Replication
- Partitioning / sharding
- NoSQL trade-offs
- Object/blob storage

### Bölüm V — Distributed Systems & System Design
- CAP ve consistency modelleri
- Replication / quorum
- Leader election
- Consensus: Raft/Paxos sezgisi
- Distributed locks
- Retry, timeout, backoff, jitter
- Circuit breaker ve load shedding
- CDC ve event-driven architecture
- Kafka ve stream processing
- Multi-region architecture
- Storage abstraction platformları (Habitat benzeri)

### Bölüm VI — Cloud, DevOps & SRE
- Linux
- Containers / Docker
- Kubernetes
- CI/CD
- Infrastructure as Code
- Load balancing
- Autoscaling
- SLI/SLO/SLA
- Incident response
- Capacity planning
- Disaster recovery

### Bölüm VII — Cybersecurity
- Threat modeling
- OWASP Top 10
- API security
- IAM / RBAC / ABAC
- Zero Trust
- TLS / PKI
- Secrets management
- Secure SDLC
- Cloud security

### Bölüm VIII — Data Engineering
- OLTP vs OLAP
- ETL / ELT
- Data lake / warehouse / lakehouse
- Batch vs streaming
- Kafka
- Spark
- CDC
- Data quality
- Data modeling

### Bölüm IX — AI / ML / LLM
- ML fundamentals
- Supervised / unsupervised learning
- Evaluation metrics
- Embeddings
- Transformers
- Attention
- LLM inference
- RAG
- Fine-tuning
- Agents/tool use
- ML system design

### Bölüm X — MLOps
- Experiment tracking
- Feature/data pipelines
- Model registry
- Deployment patterns
- Drift
- Monitoring
- GPU serving
- Batch vs online inference

### Bölüm XI — Frontend & Mobile
- Browser internals
- Rendering pipeline
- JavaScript event loop
- React/state management
- Web performance
- Mobile architecture
- Offline-first/sync

### Bölüm XII — Leadership, Product & CTO
- Technical strategy
- Architecture decision records
- Build vs buy
- Engineering metrics
- Hiring / leveling
- Roadmapping
- Reliability vs feature velocity
- Cost / performance trade-offs
- Security and compliance ownership
- Organizational design

## Seviye beklentileri

| Seviye | Tipik beklenti |
|---|---|
| Junior | Temel kavramı doğru tanımlar, küçük problemi çözer, kod kalitesine dikkat eder. |
| Mid | Bağımsız implementation yapar, debugging ve temel trade-off'ları açıklar. |
| Senior | Production failure mode'larını, performansı, güvenliği ve bakım maliyetini düşünür. |
| Staff | Birden çok takım/sistem arasındaki mimari trade-off'ları ve blast radius'u yönetir. |
| Principal | Organizasyon çapında teknik yön, standartlar ve uzun vadeli platform kararları üretir. |
| Engineering Manager | İnsan, süreç, teslimat, kalite ve teknik risk arasında denge kurar. |
| CTO | Teknoloji stratejisini ürün, şirket ekonomisi, risk, regülasyon ve organizasyonla birlikte yönetir. |

## Saatlik çalışma notları

`daily/YYYY-MM-DD/HH-00.md` altında her saat iki adet yaklaşık 30 dakikalık çalışma paketi yayınlanır. Konular gün içinde mümkün olduğunca tekrar etmeden döndürülür.

## Kaynak politikası

Öncelik sırası: **resmi dokümantasyon → akademik makale / standart → güçlü mühendislik blogu → güvenilir eğitim kaynağı**. Değişebilen veya piyasaya ilişkin iddialarda güncel kaynak kontrolü yapılır. “En çok sorulan” gibi ifadeler kesin istatistik varmış gibi kullanılmaz; farklı şirket ve kaynaklarda tekrar eden yüksek getirili konu kümeleri önceliklendirilir.

## Lisans / katkı

Bu repo eğitim amaçlı özgün notlardan oluşur. Harici kaynaklardan uzun metinler kopyalanmaz; kaynaklar bağlantı ile gösterilir. Görseller mümkün olduğunca özgün diyagram olarak üretilir veya resmi kaynağa bağlantı verilir.
