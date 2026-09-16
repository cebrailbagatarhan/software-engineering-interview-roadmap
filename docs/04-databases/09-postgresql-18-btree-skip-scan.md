# PostgreSQL 18 B-tree Skip Scan & Multicolumn Index Trade-offs

## Konu anlatımı
PostgreSQL 18 B-tree skip scan, multicolumn index'te leading column predicate'i bulunmadığında bazı sorguların yine de verimli index navigation yapabilmesini sağlar. `(x,y)` ve `WHERE y=7700` için planner, `x` değerlerini dinamik equality constraint gibi ele alıp tekrarlı `(x=N,y=7700)` aramaları yapabilir.

Leading column distinct-count düşükse bu yaklaşım index'in büyük bölümünü atlayabilir. Cardinality yüksekse repeated seek maliyeti büyür ve sequential scan daha ucuz olabilir. Skip scan leftmost-prefix sezgisini ortadan kaldırmaz; cost-based bir optimizasyondur.

## Mental model
```text
index (x,y), predicate y=?

x=A -> seek(A,y)
x=B -> seek(B,y)
x=C -> seek(C,y)

low NDV(x)  -> attractive
high NDV(x) -> expensive repeated seeks
```

## İçeride ne oluyor?
Planner eksik leading equality için dynamic equality üretip B-tree içinde repositioning yapabilir. Alternatifler single-column index, bitmap index combination veya farklı column order'dır. Her index read performansını iyileştirebilir fakat write amplification, disk ve maintenance maliyeti ekler.

## Mülakat soruları
- `(x,y)` index'i `WHERE y=?` için nasıl kullanılabilir?
- Skip scan hangi dağılımda avantajlıdır?
- Planner neden her zaman seçmez?
- Bitmap index combination farkı nedir?
- Composite vs ayrı index'ler nasıl seçilir?
- Senior: statistics yanlışı planı nasıl bozar?

## Beklenen cevap seviyesi
Junior/Mid: composite index ve leading-column sezgisi. Senior: NDV/selectivity, seek cost, bitmap ve write cost. Staff: workload index portfolio ve upgrade regression. Principal/CTO: storage/write economics ile latency SLO.

## Mini alıştırma
10M row tabloda `x` için 8 ve 500K distinct değer senaryolarını karşılaştır; `WHERE y=?` skip scan kararını açıkla.

## Proje fikri
`pg-skip-scan-lab`: PostgreSQL 18'de NDV'yi değiştirip `EXPLAIN (ANALYZE, BUFFERS)` ile plan, latency ve buffer reads karşılaştır.

## Production bağlantısı / failure modes
Skip scan'i garanti sanmak; stale statistics; yanlış skew; gereksiz index write amplification; ORDER BY ihtiyacını unutmak; major-version upgrade regression test etmemek. Plan shape, estimated/actual rows, buffers, index size, write latency ve p95/p99 izle.

## Kaynaklar
- https://www.postgresql.org/docs/18/indexes-multicolumn.html
- https://www.postgresql.org/docs/18/release-18.html
- https://www.postgresql.org/docs/18/indexes-bitmap-scans.html
