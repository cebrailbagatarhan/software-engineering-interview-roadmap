# Go 1.27 Size-Specialized Allocation, Escape Analysis & GC Economics

## Neden önemli?
Runtime allocator optimizasyonu ile application performansını ayırabilmek backend mülakatlarında güçlü bir performance-engineering sinyalidir. Go 1.27, 80 byte'tan küçük belirli heap allocation'ları için size-specialized allocation yolları ekledi. Go ekibinin 16 Eylül 2026 tarihli ölçümlerinde bu allocation'lar %20–30 daha hızlı olabilirken allocation-heavy programların toplam hızlanması yaklaşık %1'e kadar çıkabiliyor.

## Mental model
```text
value -> escape analysis -> stack
                    \
                     -> heap -> allocator -> GC

app speedup ≈ affected CPU fraction × local optimization
```

Önce allocation'ın gerekli olup olmadığını sor. Heap'e kaçış gerekiyorsa allocator maliyeti, heap growth ve GC etkisini birlikte ölç.

## Internals
Compiler, lifetime ve pointer escape davranışına göre değerleri stack veya heap'e yerleştirir. Heap allocation runtime allocator'dan geçer. Go 1.27 küçük ve bilinen size class'lar için daha özel yollar kullanarak generic allocation path üzerindeki bazı işleri azaltır. Bu optimizasyon allocation sayısını ortadan kaldırmaz ve GC'nin live-object graph tarama maliyetini otomatik çözmez.

## Mülakat soruları
- Stack ve heap allocation farkı nedir?
- Escape analysis neden vardır?
- %25 allocator microbenchmark kazancı neden %25 servis kazancı değildir?
- Allocation rate GC'yi nasıl etkiler?
- Object pool ne zaman memory retention yaratır?
- Senior: `allocs/op`, `B/op`, ns/op ve p99 nasıl birlikte yorumlanır?
- Staff: runtime upgrade canary'sinde representative workload nasıl seçilir?

## Seviye beklentisi
Junior stack/heap ve GC'yi; Mid escape analysis ve benchmark'ı; Senior allocation profile, cache/GC ve tail latency'yi; Staff fleet rollout ve canary ekonomisini; Principal/CTO performance-per-dollar ile complexity trade-off'unu açıklamalıdır.

## Mini alıştırma
CPU'nun %12'si allocation yolunda ve bu bölüm %25 hızlanıyor. Amdahl sezgisiyle toplam kazancın birkaç yüzde puanı mertebesinde kalmasını hesapla; GC azalırsa sonucun neden değişebileceğini tartış.

## Proje
Go 1.26/1.27 üzerinde 16/32/64/128-byte object workload'ları benchmark et. `ns/op`, `allocs/op`, `B/op`, GC CPU, heap live size ve service p99 kaydet; escape-analysis çıktısıyla iki heap escape'i refactor et.

## Failure modes / production
Microbenchmark genellemesi, pooling kaynaklı retention, GC ve p99'u ölçmeme, representative traffic olmadan fleet rollout. Production'da allocation bytes/sec, objects/sec, GC CPU, live heap, CPU/request ve p95/p99 birlikte izlenmelidir.

## Kaynaklar
- https://go.dev/blog/size-specialized-allocations
- https://go.dev/doc/go1.27
- https://go.dev/doc/gc-guide
