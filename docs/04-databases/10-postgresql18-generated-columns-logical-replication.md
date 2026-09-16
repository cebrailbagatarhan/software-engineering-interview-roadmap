# PostgreSQL 18 Generated Columns & Logical Replication

## Mental model
Generated column uygulamanın yazdığı bağımsız state değil, base row'dan türetilen değerdir. `STORED` write-time'da hesaplanıp saklanır; `VIRTUAL` read-time'da hesaplanır ve PostgreSQL 18'de default'tur.

```text
base columns -> generation expression -> derived value
                  | STORED: write+disk
                  | VIRTUAL: read+CPU
                  v
             publication boundary
```

## PostgreSQL 18 replication semantics
PostgreSQL 18 stored generated column değerlerinin logical replication ile yayınlanmasına izin verir. Default publication generated columns yayınlamaz. `publish_generated_columns=stored` veya explicit column list ile opt-in yapılır. Explicit column list publication option üzerinde önceliklidir.

Subscriber hedef kolonu da generated ise subscriber kendi expression'ını hesaplar; publisher generated değeri uygulanmaz. Published generated value'yu regular target column'a taşımak heterojen CDC target'larında yararlıdır. Virtual generated columns bu mekanizmayla publish edilmez. Pre-18 subscriber initial synchronization generated column değerlerini kopyalamaz.

## Interview checklist
- Virtual vs stored: read CPU, write CPU, storage, index/use-case trade-off.
- Generated value ile generation expression aynı şey değildir.
- Publication semantics schema semantics'ten ayrıdır.
- Subscriber expression drift correctness problemi olabilir.
- Mixed-version upgrade initial-sync davranışını test etmelidir.
- Birden fazla publication'da farklı column list kombinasyonları replication error üretebilir.

## Production failure modes
Schema migration ile generated expression değişirken publisher/subscriber rollout sırası; pre-18 subscriber; yanlış `publish_generated_columns` varsayımı; generated-to-generated target'ta source value'nun taşınacağını sanmak; column-list drift. Replication lag, apply conflicts, publication config ve schema/version drift gözlenmelidir.

## Mini lab
İki PostgreSQL 18 instance üzerinde `total GENERATED ALWAYS AS (price*quantity) STORED` kur. Default publication, `publish_generated_columns=stored`, explicit column list ve regular subscriber target senaryolarını karşılaştır.

## Kaynaklar
- PostgreSQL 18 Generated Columns: https://www.postgresql.org/docs/18/ddl-generated-columns.html
- Generated Column Replication: https://www.postgresql.org/docs/18/logical-replication-gencols.html
- CREATE PUBLICATION: https://www.postgresql.org/docs/18/sql-createpublication.html
- PostgreSQL 18 Release Notes: https://www.postgresql.org/docs/18/release-18.html
