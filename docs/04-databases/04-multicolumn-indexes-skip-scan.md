# Multicolumn B-tree Indexes & Skip Scan

## Mental model
Composite B-tree index lexicographic bir sıralamadır. `(a,b,c)` için leading equality koşulları ve ilk range koşulu taranacak index bölümünü güçlü biçimde daraltır. PostgreSQL 18 uygun maliyet/cardinality durumlarında eksik leading equality için skip scan kullanabilir; bu bir garanti değil planner optimizasyonudur.

```text
(a=1,b=1) ... (a=1,b=9)
(a=2,b=1) ... (a=2,b=9)
WHERE b=7 -> planner uygun görürse her a grubu için yeniden arama
```

## Interview depth
Mid: kolon sırası ve equality/range. Senior: selectivity, EXPLAIN, write amplification, skip-scan cost. Staff: workload genelinde index portfolio ve storage/cache maliyeti.

## Production trade-offs
Her query varyantına index eklemek write amplification, cache pressure ve maintenance maliyeti yaratır. Planner kararlarını gerçek veri dağılımı ve güncel statistics ile `EXPLAIN (ANALYZE, BUFFERS)` üzerinden doğrula.

## Kaynak
- https://www.postgresql.org/docs/18/indexes-multicolumn.html
