# B+Tree — Fan-out, Page Split, Range Scan ve Index Economics

## Mental model
```text
                 [20 | 50]
               /     |      \
      [2 8 14] <-> [20 31 44] <-> [50 61 79]
point: root -> leaf
range: seek -> leaf siblings
```

B+Tree page-oriented ordered index'tir. Yüksek fan-out tree height ve gerekli page I/O sayısını düşürür. Internal pages yönlendirir; leaf pages ordered entries taşır. Bu yapı equality yanında range scan ve ordered traversal için güçlüdür. PostgreSQL B-tree equality/range predicate'lerini destekler; B-tree ayrıca sorted output sağlayarak uygun `ORDER BY ... LIMIT` sorgularında explicit sort'u önleyebilir.

## Internals
- Fan-out page size ile key/pointer boyutuna bağlıdır.
- Full leaf insert split yaratabilir; separator parent'a propagate olabilir.
- Range scan başlangıç leaf'ini bulup sibling pages üzerinden ilerler.
- Index read hızını write amplification, storage ve cache pressure karşılığında satın alır.
- Düşük selectivity'de sequential scan daha ucuz olabilir.

## Mülakat soruları
1. B+Tree neden binary tree yerine disk indexlerinde kullanılır?
2. Fan-out neyi optimize eder?
3. Range scan neden verimlidir?
4. Page split maliyeti nedir?
5. Index neden her sorguyu hızlandırmaz?
6. Staff/Principal: index budget'ı workload ve storage economics ile nasıl yönetirsin?

## Seviye beklentisi
Junior ordered tree ve leaf/internal ayrımını; Mid fan-out/split/range scan'i; Senior selectivity/cache/write amplification'ı; Staff/Principal workload economics, concurrency ve governance'ı açıklamalıdır.

## Alıştırma ve proje
8 KiB page ve yaklaşık 32-byte entry için kaba fan-out hesapla. Ardından küçük page tabanlı B+Tree yaz; point/range lookup ve split ekleyip sorted-array/hash-map baseline ile benchmark et.

## Failure modes / production
Her kolona index eklemek write/storage maliyetini büyütür. Random write, low selectivity, cache miss ve stale statistics avantajı silebilir. Query plan, index size, cache hit, write throughput ve split/bloat sinyallerini birlikte izle.

## Kaynaklar
- https://www.postgresql.org/docs/18/btree.html
- https://www.postgresql.org/docs/18/indexes-ordering.html
- https://www.postgresql.org/docs/current/indexes-types.html
