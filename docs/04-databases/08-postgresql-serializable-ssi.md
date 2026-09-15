# PostgreSQL Serializable Isolation, SSI & Retry Discipline

## Konu anlatımı
PostgreSQL `SERIALIZABLE`, concurrent transaction sonuçlarını bir serial execution ile uyumlu tutmayı hedefler. Serializable Snapshot Isolation (SSI), read/write bağımlılıklarını izleyip tehlikeli dependency yapıları oluştuğunda transaction'lardan birini serialization failure ile abort edebilir. Predicate/SIRead lock'lar normal blocking row lock değildir; dependency tespiti içindir ve `pg_locks` içinde `SIReadLock` olarak görülebilir.

Correctness protokolünün uygulama tarafı retry'dır: serialization failure alan business transaction baştan tekrar çalıştırılmalıdır. Dış side-effect'ler retry altında duplicate olmamalıdır. Uzun read-only işler için `SERIALIZABLE READ ONLY DEFERRABLE` güvenli snapshot bekleyebilir. Serializable garantisinin hot standby/logical replica okumalarına aynı biçimde uzanmadığı unutulmamalıdır.

## Mental model
```text
T1 read P -------- write A
      \\ rw-dependency
T2 ---- write P --- read A

unsafe dependency graph -> abort one -> retry whole transaction
```

## Mülakat soruları
- Serializable ile Repeatable Read farkı?
- SIRead lock neden blocking lock değildir?
- Serialization failure neden retry ister?
- External side-effect transaction retry'sinde nasıl korunur?
- Contention yükseldiğinde abort/latency nasıl gözlemlenir?

## Beklenen cevap seviyesi
Mid: isolation/anomaly/retry. Senior: SSI, idempotency ve retry boundary. Staff: contention, retry budget, replica caveat'ları ve invariant tests.

## Mini alıştırma
Write-skew üreten iki concurrent transaction çiz ve Serializable'da hangi noktada retry gerektiğini göster.

## Proje fikri
`ssi-race-lab`: concurrent reservation invariant'ını üç isolation level altında test et; abort/retry metriği ekle.

## Production bağlantısı ve failure modes
Retry'siz Serializable; yalnız son statement'ı retry; transaction içinde non-idempotent external side-effect; replica okumalarına primary garantisini varsaymak; abort rate'i izlememek.

## Kaynaklar
- https://www.postgresql.org/docs/18/transaction-iso.html
- https://www.postgresql.org/docs/18/mvcc-caveats.html
- https://www.postgresql.org/docs/18/runtime-config-client.html
