# PostgreSQL 18 B-tree Skip Scan & Composite Index Design

PostgreSQL 18, multicolumn B-tree index'lerde leading column için equality predicate bulunmayan bazı sorguların index'i daha etkili kullanmasını sağlayan skip scan desteğini geliştirdi.

## Mental model

```text
index (a,b)
(a=1) -> seek b=x
(a=2) -> seek b=x
(a=3) -> seek b=x
...
```

Planner, leading key'in olası değer grupları boyunca tekrarlı index aramaları yaparak sonraki kolon predicate'inden yararlanabilir. Bu yüzden `(a,b)` index'i bazı `WHERE b = ?` sorgularında klasik left-prefix sezgisinin ötesinde kullanılabilir.

## Cost model sezgisi
Leading column distinct cardinality düşükse birkaç seek ucuz olabilir. Cardinality çok yüksekse tekrarlı seek maliyeti full/bitmap/sequential scan'den pahalı olabilir. Statistics ve selectivity bu kararın merkezindedir.

Skip scan, 'column order artık önemsiz' anlamına gelmez. Equality/range predicate düzeni, ORDER BY gereksinimi, index size, cache locality ve write amplification hâlâ composite index tasarımını belirler. Dedicated `(b)` index daha hızlı olabilir fakat ek storage ve write cost yaratır.

## Interview checkpoints
- Left-prefix rule neyi anlatır?
- Skip scan hangi query shape'inde yardımcı olur?
- Leading-column NDV maliyeti nasıl değiştirir?
- Planner statistics neden kritiktir?
- Dedicated secondary index ile skip scan trade-off'u nedir?

## Production failure modes
Skip scan'i garanti kabul etmek, stale statistics, yalnız read benchmark yapmak, redundant index'leri korumak ve plan regression'larını gözlemlememek sık hatalardır. Query p95/p99, buffer reads, plan changes, index size, write TPS, autovacuum ve statistics freshness birlikte izlenmelidir.

## Kaynaklar
- https://www.postgresql.org/docs/18/release-18.html
- https://www.postgresql.org/about/news/postgresql-18-released-3142/
- https://www.postgresql.org/docs/18/indexes-multicolumn.html
