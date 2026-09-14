# High-Yield Interview Questions — Foundations, Networking, Backend

Bu dosya kesin bir global sıralama iddiası taşımaz. Ama backend, platform, infrastructure, systems ve general software engineering görüşmelerinde tekrar eden **yüksek getirili soru kalıplarını** toplar.

Her soruda hedef sadece cevabı bilmek değil; interviewer'ın hangi düşünme biçimini ölçtüğünü anlamaktır.

---

# 1. Computer Systems

## Junior

### 1. Process ile thread arasındaki fark nedir?

**Beklenen:** process isolation + address space; thread'lerin aynı process içinde memory paylaşabilmesi.

**Follow-up:** Thread kullanmak neden tehlikeli olabilir?

**Interviewer ne ölçüyor?** Shared state ve concurrency farkındalığı.

---

### 2. Stack ve heap nedir?

**Beklenen:** lifetime, call frames, dynamic allocation.

**Kötü cevap:** “Stack hızlı, heap yavaş.”

**Daha iyi cevap:** Allocation ve ownership modelini, cache/locality ve runtime ayrıntılarının performansı etkilediğini söyle.

---

### 3. CPU cache ne işe yarar?

**Beklenen:** CPU-RAM latency farkını azaltır; temporal/spatial locality kullanır.

**Follow-up:** Array neden linked list'ten pratikte daha hızlı olabilir?

---

## Mid

### 4. Context switch neden maliyetlidir?

**Beklenen:** execution state + scheduler + cache/TLB locality etkisi.

### 5. Race condition nedir?

**Beklenen:** outcome'un timing/interleaving'e bağlı hale gelmesi.

### 6. Deadlock nasıl oluşur?

**Beklenen:** circular wait ve lock ordering.

---

## Senior+

### 7. CPU %100 ama throughput artmıyor. Nasıl debug edersin?

**Güçlü cevap sırası:**

```text
profiling
→ flame graph
→ lock contention
→ allocation / GC
→ syscalls
→ run queue
→ cache misses
→ algorithmic hot path
```

**Interviewer ne ölçüyor?** Ölçmeden optimize etmeme disiplini.

### 8. 100k concurrent connection için nasıl concurrency modeli seçersin?

**Beklenen:** runtime, event loop, async I/O, thread/goroutine maliyeti, backpressure ve workload tipi.

---

# 2. Networking

## Junior

### 9. TCP ve UDP farkı nedir?

**Beklenen:** ordered/reliable byte stream vs datagram semantics.

**Kötü cevap:** “TCP yavaş, UDP hızlı.”

### 10. DNS nedir?

**Beklenen:** distributed naming system; resolver/cache/authoritative server kavramlarına giriş.

### 11. HTTP ile HTTPS farkı nedir?

**Beklenen:** TLS ile confidentiality, integrity, authentication.

---

## Mid

### 12. Browser'a URL yazınca ne olur?

İyi cevapta yaklaşık şu zincir olmalı:

```text
DNS
→ network route
→ TCP/QUIC
→ TLS
→ HTTP
→ LB/CDN/proxy
→ application
→ database/dependencies
→ response
```

### 13. Keep-alive neden performansı artırabilir?

Connection setup/TLS maliyetini amortize eder.

### 14. L4 ve L7 load balancer farkı nedir?

Transport-level routing vs application-aware routing.

---

## Senior+

### 15. p50 40 ms ama p99 2 saniye. Nereden başlarsın?

Beklenen yaklaşım:

- distributed tracing,
- queueing,
- connection pool,
- downstream p99,
- retries,
- DB locks,
- network/TLS/DNS.

### 16. Retry neden sistemi çökertir?

**Beklenen:** retry amplification, synchronized retries, dependency saturation.

### 17. Connection pool kaç olmalı?

**Doğru yaklaşım:** tek sayı ezberleme. Downstream capacity, concurrency, query latency ve queueing üzerinden düşün.

---

# 3. Backend

## Junior

### 18. Cache nedir?

Latency ve backend load azaltma.

### 19. Authentication ve authorization farkı nedir?

```text
Authentication: Kimsin?
Authorization: Bunu yapabilir misin?
```

### 20. Rate limiting neden kullanılır?

Abuse, fairness, capacity protection, quota.

---

## Mid

### 21. Cache-aside pattern nasıl çalışır?

Hit/miss ve DB fallback çiz.

### 22. Cache invalidation nasıl yapılır?

TTL, explicit invalidation, write-through veya event-driven yaklaşım; trade-off konuş.

### 23. Token bucket nasıl çalışır?

Capacity + refill rate + token consumption.

### 24. Idempotency key ne işe yarar?

Payment/create request retry'da duplicate side effect'i önler.

### 25. Circuit breaker nedir?

Fail eden dependency'ye request yağdırmayı geçici olarak keser.

---

## Senior

### 26. Cache stampede nedir?

Popüler key expire → aynı anda çok sayıda miss → DB overload.

**Çözümler:** single-flight, TTL jitter, stale-while-revalidate, prewarm.

### 27. Distributed rate limiter nasıl tasarlanır?

**Interviewer ne ölçüyor?** Accuracy/availability/latency trade-off'u.

### 28. Queue neden bounded olmalı?

Unbounded queue overload'u gizler; latency/memory birikir.

### 29. Timeout değerini nasıl seçersin?

SLO + downstream latency distribution + deadline propagation üzerinden.

### 30. Hangi request retry edilmemeli?

Permanent validation/auth errors ve idempotent olmayan unsafe operation'lar dikkat gerektirir.

---

# 4. Staff / Principal

### 31. Cache cluster tamamen çökerse database'i nasıl korursun?

Güçlü cevapta:

- degraded mode,
- stale cache,
- local cache,
- request collapse,
- load shedding,
- rate limits,
- capacity reserve

olabilir.

### 32. 1000 tenant'lı platformda noisy neighbor nasıl engellenir?

- per-tenant quota,
- concurrency limits,
- weighted fairness,
- resource isolation,
- admission control.

### 33. Merkezi platform ne zaman iyi fikir, ne zaman tehlikeli?

**Artılar:** standardization, velocity, policy consistency.

**Eksiler:** coupling, blast radius, organizational bottleneck.

### 34. Multi-region failover sırasında data consistency nasıl etkilenir?

RPO/RTO, replication lag, writes during partition, conflict resolution konuş.

### 35. Distributed lock gerçekten gerekli mi?

Önce ownership, partitioning, optimistic concurrency veya idempotent workflow ile lock'u kaldırmanın mümkün olup olmadığını sorgula.

---

# 5. Engineering Manager / CTO

### 36. Build vs buy kararını nasıl verirsin?

- strategic differentiation,
- total cost of ownership,
- hiring/skills,
- operational load,
- vendor risk,
- migration cost,
- compliance.

### 37. Reliability yatırımını nasıl önceliklendirirsin?

Incident frequency × impact × probability + business SLO + engineering cost.

### 38. Platform ekibi ne zaman kurulmalı?

Aynı altyapı problemini çok sayıda takım tekrar çözüyor ve standardization net değer yaratıyorsa.

### 39. Performance optimization'a ne zaman yatırım yapılmalı?

Profiling + business/SLO + cost data olmadan premature optimization yapma.

### 40. Teknik olarak yapılabiliyor olması neden yeterli değildir?

CTO seviyesinde karar:

```text
technical feasibility
+ business value
+ risk
+ cost
+ time
+ organization capability
= decision
```

---

# Nasıl kullanılmalı?

Her gün 5 soru seç:

1. 60 saniyede kısa cevap ver.
2. 5 dakikada whiteboard cevabı ver.
3. En az iki trade-off ekle.
4. En az bir failure mode ekle.
5. Senior+ için production example ekle.

Bir soruyu ezberlediğinde değil, follow-up gelince de reasoning yapabildiğinde öğrenmiş say.
