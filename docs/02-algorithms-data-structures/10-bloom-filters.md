# Bloom Filters, False Positives & Memory Economics

Bloom filter, membership sorgusunda `definitely absent` veya `maybe present` cevabı veren probabilistic veri yapısıdır. Bit array ve `k` hash kullanır. Klasik tasarım false positive üretebilir; doğru uygulanmış ve silme yapılmayan klasik Bloom filter false negative üretmemelidir.

```text
key -> k hashes -> bit array
                  /       \
             any zero    all one
                |           |
          absent kesin   maybe present
```

Yaklaşık false-positive olasılığı `p ≈ (1-e^(-kn/m))^k`; sabit `m,n` için optimum `k ≈ (m/n) ln 2`. Filtre source of truth değil, pahalı negative lookup'ları azaltan ön kapıdır.

## Interview depth
- Junior: bit array ve membership.
- Mid: false positive/negative ve memory trade-off.
- Senior: sizing, saturation, deletion, rebuild.
- Staff: shard/global filter, replication, stale-state yönetimi.
- Principal/CTO: RAM maliyeti ile downstream DB/I/O maliyeti.

## Failure modes
Kapasiteyi aşmak; filtreyi authoritative sanmak; bit sıfırlayarak delete yapmak; rebuild sırasında yeni key kaçırmak; observed FP rate'i ölçmemek.

## Production metrics
Fill ratio, estimated/observed FP rate, avoided backend lookup, rebuild duration, memory bytes ve downstream QPS.

## Kaynaklar
- https://www.eecs.harvard.edu/~michaelm/postscripts/im2005b.pdf
- https://research.google/pubs/summary-cache-a-scalable-wide-area-web-cache-sharing-protocol/
