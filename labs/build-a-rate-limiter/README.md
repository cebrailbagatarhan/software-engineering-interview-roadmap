# Lab — Build a Production-Minded Rate Limiter

Bu lab'in amacı sadece algoritma yazmak değil; **capacity protection, fairness, concurrency ve distributed state** problemlerini küçük ölçekte deneyimlemektir.

## Hedef API

```text
allow(key) -> true / false
```

Örnek:

```text
allow("user:42") -> true
allow("user:42") -> true
allow("user:42") -> false
```

---

## Aşama 1 — Fixed Window

İlk sürüm:

```text
window = 60 seconds
limit = 100 requests
```

State:

```text
key -> current_window_start, count
```

Test et:

- 99 request,
- 100 request,
- 101 request,
- window boundary.

### Gözlem

Window boundary çevresinde burst oluşabilir.

---

## Aşama 2 — Token Bucket

State:

```text
capacity
refill_rate
current_tokens
last_refill_time
```

Pseudo-code:

```text
function allow(key):
    refill(key)

    if tokens[key] >= 1:
        tokens[key] -= 1
        return true

    return false
```

### Testler

1. Uzun idle süre sonrası burst.
2. Sürekli sabit rate.
3. Limit üstü burst.
4. 100 concurrent caller.
5. Aynı key ve farklı key'ler.

---

## Aşama 3 — Thread Safety

İki request aynı anda şu durumu görürse ne olur?

```text
tokens = 1

Thread A reads 1
Thread B reads 1
Thread A decrements
Thread B decrements
```

Atomic update veya lock gereksinimini incele.

Ölç:

- lock contention,
- throughput,
- p95 latency.

---

## Aşama 4 — HTTP Service

Endpoint:

```http
GET /resource
X-API-Key: demo-user
```

Limit aşılırsa:

```http
HTTP/1.1 429 Too Many Requests
```

İstersen `Retry-After` header'ı ekle.

---

## Aşama 5 — Metrics

Şu metrikleri üret:

```text
requests_total
requests_allowed_total
requests_rejected_total
active_keys
rate_limit_check_latency
```

Ek olarak p50/p95/p99 ölç.

---

## Aşama 6 — Distributed Version

Artık iki instance çalıştır:

```text
Client
  ↓
Load Balancer
 ├─ Limiter/API-1
 └─ Limiter/API-2
```

### Problem

Her instance local state tutarsa global limit iki katına çıkabilir.

Örneğin hedef:

```text
100 req/min global
```

Ama iki instance ayrı ayrı 100 izin verirse:

```text
~200 req/min
```

### Seçenek A — Shared Redis/Valkey

```text
API-1 ─┐
       ├─ Redis / Valkey
API-2 ─┘
```

Avantaj:
- merkezi state,
- daha doğru global limit.

Risk:
- network latency,
- shared dependency,
- hot key,
- cache/store outage.

### Seçenek B — Local Budget Leasing

Global quota parçalarını instance'lara lease et:

```text
Global 1000 token
   ├─ API-1: 200
   ├─ API-2: 200
   ├─ API-3: 200
   └─ reserve: 400
```

Daha az merkezi round trip ama accuracy düşebilir ve rebalance gerekir.

---

## Aşama 7 — Failure Injection

Bilerek boz:

1. Shared store'a 100 ms latency ekle.
2. Store'u tamamen kapat.
3. Tek bir key'e aşırı trafik gönder.
4. Clock skew simüle et.
5. API instance'larından birini öldür.

Her durumda karar ver:

```text
fail-open mı?
fail-closed mı?
```

Örneğin login brute-force protection ile ücretsiz public API quota aynı policy'yi kullanmak zorunda değildir.

---

# README'de cevaplanması gereken mülakat soruları

1. Neden token bucket seçtin?
2. Burst'e nasıl davranıyor?
3. Thread-safe mi?
4. Distributed hale gelince hangi guarantee değişti?
5. Redis/Valkey çökerse ne oluyor?
6. Hot key oluşursa ne yaparsın?
7. Multi-region olursa global limit nasıl uygulanır?
8. Accuracy ile availability arasında hangi trade-off var?
9. Tenant başına farklı limit nasıl verirsin?
10. Rate limiter kendisi bottleneck olursa ne yaparsın?

---

# Staff-level genişletme

Aşağıdakileri eklemeyi dene:

- hierarchical quotas: org -> team -> user,
- weighted limits,
- endpoint-specific cost,
- concurrency limiting,
- distributed approximate counters,
- configuration hot reload,
- audit/decision logs,
- dashboard.

Örneğin her operation aynı maliyette olmayabilir:

```text
GET /profile      cost = 1
POST /search      cost = 5
POST /ai/generate cost = 20
```

Bu durumda limiter request sayısı yerine **cost unit** tüketebilir.

---

# Habitat bağlantısı

Habitat gibi çok tenant'lı merkezi storage platformunda rate limiting yalnızca abuse koruması değildir.

Aynı zamanda:

- noisy-neighbor control,
- backend protection,
- fair resource allocation,
- regional capacity management,
- expensive operation shaping

için kullanılır.

Bu lab'i tamamladıktan sonra şu soruya cevap verebilmelisin:

> Binlerce client'ın kullandığı merkezi storage gateway için rate limiter'ı nasıl tasarlarım ve limiter'ın kendisinin single point of failure olmasını nasıl engellerim?

---

# Kaynaklar

- RFC 6585 — 429 Too Many Requests: https://www.rfc-editor.org/rfc/rfc6585
- Google SRE Book — Handling Overload: https://sre.google/sre-book/handling-overload/
- AWS Builders Library — Timeouts, retries and backoff with jitter: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- Valkey documentation: https://valkey.io/topics/

## Bitirme kriteri

Lab “çalışıyor” diye bitmiş sayılmaz. Şunlar varsa bitmiştir:

- tests,
- benchmark,
- failure injection,
- metrics,
- architecture diagram,
- trade-off açıklaması,
- production'da neyi farklı yapardın bölümü.
