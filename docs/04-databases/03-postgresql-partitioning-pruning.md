# PostgreSQL Declarative Partitioning & Partition Pruning

## Mental model
Tek mantıksal tablo, partition key ile fiziksel child tablolara yönlenir. İyi sorgu predicate'i optimizer'ın ilgisiz child'ları prune etmesini sağlar.

```text
parent events
  -> 2026-07
  -> 2026-08
  -> 2026-09 <- query target
```

## Temel noktalar
PostgreSQL RANGE, LIST ve HASH declarative partitioning destekler. Parent storage tutmaz. Partitioning index'in yerine geçmez; partition içinde uygun index'ler hâlâ önemlidir. Partition pruning plan veya execution aşamasında ilgisiz partition'ları eleyebilir. Retention işlerinde eski partition'ı detach/drop etmek büyük DELETE operasyonlarına göre operasyonel avantaj sağlayabilir.

## Interview depth
Senior aday partition key'i workload, retention, skew, query patterns ve operational lifecycle üzerinden seçebilmelidir. Staff seviyesinde future-partition automation, migration, observability ve multi-tenant blast radius tartışılmalıdır.

## Failure modes
Yanlış key, binlerce küçük partition, future partition eksikliği, skew, pruning'i engelleyen predicate ve bakım otomasyonu hataları.

## Kaynaklar
- https://www.postgresql.org/docs/18/ddl-partitioning.html
- https://www.postgresql.org/docs/18/sql-createtable.html
