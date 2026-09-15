# PostgreSQL VACUUM, HOT Updates & Visibility Map

PostgreSQL MVCC'de UPDATE/DELETE eski tuple sürümleri bırakabilir. Standart `VACUUM` reusable space, visibility/statistics bakımı ve transaction-ID wraparound koruması için kritiktir. `VACUUM FULL` tabloyu yeniden yazar ve `ACCESS EXCLUSIVE` lock gerektirdiğinden rutin çözüm değildir.

## Mental model
```text
UPDATE -> old/new tuple -> dead later
                 |
      indexed columns unchanged + same-page space
                 v
               HOT

VACUUM -> reusable space + visibility map + wraparound safety
                               |
                         all-visible page
                               v
                    index-only scan may skip heap
```

## Mülakat odağı
- Dead tuple neden oluşur?
- VACUUM ve VACUUM FULL farkı.
- Visibility Map ve index-only scan ilişkisi.
- HOT koşulları ve fillfactor trade-off'u.
- Autovacuum lag belirtileri ve tuning.

## Production
Write-heavy tablolarda `n_tup_hot_upd`, dead tuples, vacuum cadence, table/index growth ve heap fetch oranlarını birlikte izle. Fillfactor disk/cache footprint karşılığında same-page update alanı sağlar.

## Kaynaklar
- https://www.postgresql.org/docs/18/routine-vacuuming.html
- https://www.postgresql.org/docs/18/storage-vm.html
- https://www.postgresql.org/docs/18/storage-hot.html
