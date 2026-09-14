# Deadlocks, Lock Ordering ve Contention

## Temel model
Concurrency'de bekleme normal olabilir; deadlock ise wait-for graph'ta cycle oluşmasıdır. Örnek: T1 A'yı tutup B'yi bekler, T2 B'yi tutup A'yı bekler. PostgreSQL deadlock'u algılar ve işlemlerden birini abort ederek ilerlemeyi sağlar.

```text
T1 holds A -> waits B
   ^             |
   |             v
T2 waits A <- holds B
```

## Tasarım ilkeleri
- Transaction'ları kısa tut.
- Aynı kaynak kümelerini mümkün olduğunca deterministic sırada kilitle.
- Network/user interaction sırasında DB lock tutma.
- Deadlock abort'u retry edilecekse işlem idempotency'sini ve retry budget'ını düşün.
- Lock wait ile deadlock'u ayrı gözlemle; contention cycle olmadan da latency yaratabilir.

## Mülakat derinliği
Senior aday lock ordering, transaction boundary, retry ve observability'yi bağlamalıdır. Staff aday hotspot schema, admission control ve servisler arası transaction tasarımını tartışmalıdır.

## Production failure modes
Uzun transaction, hotspot row, gereksiz `FOR UPDATE`, farklı code path'lerde farklı lock sırası, sınırsız retry ve connection pool saturation.

## Habitat bağlantısı
Storage control-plane veya metadata workflow'ları aynı resource setini güncelliyorsa resource ID'lerine göre deterministic lock ordering cycle riskini azaltır. Cross-service workflow'da DB lock'u remote backend çağrısı boyunca tutmamak özellikle önemlidir.

## Kaynaklar
- PostgreSQL 18 — Explicit Locking: https://www.postgresql.org/docs/18/explicit-locking.html
- PostgreSQL 18 — pg_locks: https://www.postgresql.org/docs/18/view-pg-locks.html
