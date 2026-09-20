# Skip Lists, Probabilistic Balancing & Ordered Index Economics

## Konu anlatımı
Sorted linked list range traversal için iyidir ama search `O(n)` olur. Balanced tree `O(log n)` search/update sağlar; rotation ve strict balance invariants taşır. Skip list, base sorted list üzerinde giderek seyrekleşen forward-pointer seviyeleri kurar. Node level'ı random seçildiği için explicit rotation yerine probabilistic balancing elde edilir. Expected search/insert/delete `O(log n)` iken worst case `O(n)` kalır.

**Mental model:** üst seviyeler express lane'dir; search yukarıda büyük sıçrar, hedefi aşmadan aşağı iner.

```text
L3: HEAD --------------------------> 80
L2: HEAD --------> 20 ------------> 80
L1: HEAD -> 10 -> 20 ----> 50 ----> 80 -> 90
L0: HEAD -> 10 -> 20 ->30->50->60->80->90
```

## İçeride ne oluyor?
- Her node level 0'da vardır; yüksek level'a çıkma olasılığı geometrik olarak azalır.
- Search yüksek seviyeden başlar; next target'tan küçükse sağa, değilse aşağı gider.
- Insert predecessor/update path'i tutar, random level seçer ve forward pointer'ları splice eder.
- Expected height/operation cost `O(log n)`; worst-case shape hâlâ lineer olabilir.
- Range query başlangıcı expected `O(log n)`, ardından level 0 traversal ile toplam yaklaşık `O(log n + k)` olur.
- Redis current sorted-set implementation member lookup için hash table, ordered/range/rank görünümü için skip-list tabanlı yapı kullanır: hibrit index access pattern'leri ayırır.

## Mülakat soruları
1. Skip list neden linked list'ten hızlı search yapabilir?
2. Neden rotation gerekmez?
3. Expected ve worst-case complexity farkı nedir?
4. Insert sırasında predecessor array neden tutulur?
5. Skip list ile B-tree/red-black tree'yi cache locality, concurrency ve range scan açısından karşılaştır.
6. Point lookup + ordered range için neden hash table + ordered index hibriti kullanılır?

## Seviye beklentisi
- **Junior:** sorted list, forward pointer, random level.
- **Mid:** search/insert/delete ve expected complexity.
- **Senior:** probability parameter, memory, locality, range economics.
- **Staff/Principal:** concurrency, hybrid index ve workload-driven benchmarking.

## Alıştırma / proje
16 node ve `p=1/2` için level 0/1/2/3 beklenen node sayılarını hesapla. `skiplist-index-lab` ile 1M key üzerinde skip list, sorted array ve balanced-tree library'yi random/sorted insert, point lookup ve 100-item range scan workload'larında karşılaştır.

## Failure modes / production
Worst-case'i expected bound gibi anlatmak, RNG/level cap'i kötü seçmek, duplicate ordering semantics'ini tanımlamamak, pointer-heavy layout'un cache maliyetini ve concurrent memory reclamation'ı küçümsemek tipik hatalardır. Operation p95/p99, bytes/key, level distribution, range-scan length, allocator pressure ve contention ölçülmelidir.

## Kaynaklar
- William Pugh — A Skip List Cookbook: https://drum.lib.umd.edu/items/56c44671-3973-46b6-9e52-f71dc95af178
- William Pugh — Concurrent Maintenance of Skip Lists: https://drum.lib.umd.edu/items/3c796454-0f7b-4fef-806e-c387fdfc88a4
- Redis current sorted-set implementation: https://github.com/redis/redis/blob/unstable/src/t_zset.c
