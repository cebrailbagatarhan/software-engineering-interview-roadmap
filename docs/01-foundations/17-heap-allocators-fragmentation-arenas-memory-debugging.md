# Heap Allocators — Fragmentation, Arenas ve Memory Debugging

## Mental model
```text
application malloc/free
        |
thread cache / size classes
        |
 arena / free lists
        |
large mappings / heap regions
        |
 virtual memory -> kernel pages

fast reuse <-> retained memory
low contention <-> more caches/arenas
compact memory <-> allocation CPU cost
```

## Konu anlatımı
`malloc(128)` kernel'den tam 128 byte istemek değildir. Userspace allocator daha büyük memory region'larını işletim sisteminden alır, bunları size class/chunk'lara böler, metadata tutar ve allocation/free isteklerini mümkün olduğunca syscall yapmadan karşılar. Tasarım hız, memory footprint, fragmentation ve concurrency arasında trade-off kurar.

**Internal fragmentation**, allocator'ın verdiği block'un application'ın istediğinden büyük olmasıdır. **External fragmentation**, toplam free memory yeterli olsa bile uygun contiguous block bulunamamasıdır. Thread-local cache/arena tasarımları lock contention'ı azaltabilir fakat free memory'nin userspace allocator'da tutulmasına ve RSS'in live heap'ten yüksek kalmasına yol açabilir.

## İçeride ne oluyor?
- Alignment ve metadata usable allocation boyutunu request'ten büyütebilir.
- Size classes hızlı reuse sağlar; internal fragmentation maliyeti vardır.
- Free-list/bin yapıları boş block'ları yeniden kullanım için tutar.
- Coalescing komşu free block'ları birleştirerek external fragmentation'ı azaltabilir.
- Per-thread cache ve multiple arenas contention'ı azaltır; memory retention yükseltebilir.
- Büyük allocations ayrı mappings ile ele alınabilir; küçük allocations pooled regions'dan gelebilir.
- Application leak ile allocator retention aynı değildir: live/reachable memory, free-but-retained pages ve OS'e dönmüş pages ayrılmalıdır.
- ASan out-of-bounds/use-after-free gibi memory-safety bug'larını; LeakSanitizer unreachable leak'leri test ortamında yakalamaya yardım eder.

## Mülakat soruları
1. Stack ve heap allocation farkı nedir?
2. `free()` memory'nin hemen OS'e döndüğü anlamına gelir mi?
3. Internal ve external fragmentation farkı nedir?
4. Size classes neden kullanılır?
5. Thread cache/arena concurrency'yi nasıl iyileştirip RSS'i kötüleştirebilir?
6. Senior: memory leak ile fragmentation/retention nasıl ayrılır?
7. Staff: latency-sensitive service'te allocator seçimi nasıl benchmark edilir?

## Beklenen cevap seviyesi
- **Junior:** stack/heap, allocation/free ve leak.
- **Mid:** size classes, free lists, fragmentation ve syscall amortization.
- **Senior:** arenas, thread caches, RSS vs live heap, mappings ve profiling.
- **Staff:** allocator/workload matching, fleet memory economics, tail latency ve safe rollout.

## Mini alıştırma
24 B, 40 B ve 4 KiB allocation yapan workload'larda size-class rounding, locality ve fragmentation riskini tahmin et. Allocation/free sırasını değiştirerek external fragmentation'ın nasıl değişebileceğini çiz.

## Proje fikri
`allocator-lab`: fixed-size pool + basit segregated free-list allocator geliştir. System allocator ile throughput, p99 allocation latency, peak RSS ve fragmentation proxy'sini karşılaştır. Buggy bir target'ı ASan/LSan ile çalıştırıp use-after-free ve leak raporlarını CI artifact'ı yap.

## Failure modes / production bağlantısı
RSS artışını otomatik leak saymak, yalnız heap profiler'a bakıp native/runtime memory'yi unutmak, allocator benchmark'ını gerçek allocation-size/lifetime dağılımından koparmak ve sanitizer runtime'ını production binary'ye taşımak hatalıdır. Production'da RSS, anonymous mapped memory, allocation rate, live heap, runtime/GC memory, page faults, OOM kills ve p99 latency birlikte değerlendirilmelidir.

## Kaynaklar
- GNU C Library — Memory Allocation: https://sourceware.org/glibc/manual/latest/html_node/Memory-Allocation.html
- Clang — AddressSanitizer: https://clang.llvm.org/docs/AddressSanitizer.html
- Clang — LeakSanitizer: https://clang.llvm.org/docs/LeakSanitizer.html
- Linux man-pages — mmap(2): https://man7.org/linux/man-pages/man2/mmap.2.html
