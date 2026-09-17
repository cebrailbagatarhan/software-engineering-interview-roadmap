# Consistent Hashing, Virtual Nodes & Rendezvous Hashing

## Neden önemli?
Elastic cache ve shard fleet'lerinde `hash(key) % N`, membership değişince modulus değiştiği için yaygın remapping üretir. Consistent hashing ve rendezvous hashing, node add/remove sırasında placement churn'ünü sınırlamak için kullanılan iki temel yaklaşımdır.

## Mental model
Consistent-hash ring'de node ve key'ler aynı hash uzayındadır; key saat yönünde ilk node'a aittir. Node eklenmesi esas olarak komşu ownership range'lerini etkiler. Virtual node'lar fiziksel node başına birden çok ring position vererek skew'u azaltır.

```text
0 ------------------------------- 2^m
     N1       N2        N3
      ^        ^         ^
   local ownership movement

modulo: H(key) % N -> N değişince yaygın remap
rendezvous: owner = argmax score(key,node)
```

Rendezvous hashing her key-node çifti için deterministic score hesaplayıp en yüksek skorlu node'u seçer. Minimal remapping sağlar ve ring metadata'sı gerektirmez; naive seçim `O(N)` candidate scoring maliyeti taşır.

## Mülakat derinliği
- Junior: hash partitioning ve remapping problemi.
- Mid: ring, successor ownership, virtual nodes.
- Senior: replication, rebalance, hot keys, cache warm-up.
- Staff: weighted placement, rack/AZ awareness, membership convergence.
- Principal/CTO: routing ownership, managed-vs-build ve operational cost.

## Failure modes ve trade-off'lar
Consistent hashing perfect balance garanti etmez. Az vnode skew yaratabilir; farklı membership view'ları aynı key için farklı owner seçebilir; replica placement failure-domain aware değilse tek AZ arızası birden fazla kopyayı götürebilir. Hot key problemi placement'tan bağımsız olarak replication, request coalescing veya application-level partitioning isteyebilir.

Rebalance sırasında yalnız remap oranı değil, data-copy bandwidth ve backend load da kontrol edilmelidir. Production metrikleri: ownership skew, remap rate, rebalance bandwidth, cache hit-rate, saturation ve membership convergence time.

## Alıştırma / proje
Modulo, ring+vnodes ve rendezvous implement et. 4 -> 5 node geçişinde 100k key için remap yüzdesi ve key-count variance ölç; weighted node ve replication factor ekle.

## Kaynaklar
- https://dl.acm.org/doi/10.1145/258533.258660
- https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf
- https://www.eecs.umich.edu/techreports/cse/96/CSE-TR-316-96.pdf
