# Rollback Union-Find & Offline Dynamic Connectivity

## Problem
Klasik DSU `union/find` ile monotonik birleşmeleri çok iyi çözer fakat edge deletion doğal değildir. Bütün event stream önceden biliniyorsa edge'lerin aktif zaman aralıklarını çıkarıp zaman üzerinde segment tree kurarak deletion probleminden kaçınılabilir.

```text
edge active interval -> segment-tree nodes
                         |
                       DFS
                  enter: union
                  leaf: query
                  exit: rollback
```

## Rollback DSU
Parent ve size/rank değişikliklerini history stack'e kaydet. `snapshot()` stack uzunluğunu verir; `rollback(snapshot)` değişiklikleri tersine sarar. Union-by-size tree yüksekliğini logaritmik tutar.

Kritik ayrıntı: path compression rollback'i zorlaştırır çünkü `find` birçok parent pointer'ını mutate eder. Rollback DSU bu nedenle genellikle path compression kullanmaz.

## Offline dynamic connectivity
Her `add(edge)` ile karşılık gelen `remove(edge)` arasını half-open interval olarak düşün. Interval'i segment tree'nin O(log Q) düğümüne ekle. DFS sırasında o node'un edge'lerini union et, leaf query'lerini cevapla, çıkışta snapshot'a rollback yap.

Q event ve N vertex için tipik maliyet O(Q log Q log N) civarındadır. Online cevap zorunluysa bu yaklaşım uygun değildir; daha karmaşık dynamic-tree yapıları veya farklı recomputation stratejileri gerekir.

## Mülakat ekseni
- DSU deletion neden zor?
- rollback history hangi mutation'ları taşır?
- path compression neden kullanılmaz?
- active interval decomposition
- duplicate/multiedge semantics
- offline vs online trade-off

## Failure modes
No-op union history invariant'ını bozmak; interval sınırlarını karıştırmak; duplicate edge semantics tanımlamamak; recursion depth; offline çözümü streaming requirement'a uygulamak.

## Mini proje
Event stream CLI yaz; rollback DSU sonucunu küçük random graph'larda naive BFS oracle ile karşılaştır. History depth ve operation count ölç.

## Kaynaklar
- https://algs4.cs.princeton.edu/15uf/
- https://cp-algorithms.com/data_structures/deleting_in_log_n.html
- https://cp-algorithms.com/data_structures/disjoint_set_union.html
