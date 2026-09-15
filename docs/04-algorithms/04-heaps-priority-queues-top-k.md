# Heaps, Priority Queues & Top-K

## Temel model
Min-heap complete binary tree'dir ve her parent çocuklarından küçük/eşittir. Array representation cache-friendly ve kompakt bir uygulama sağlar. Kök extremumdur; yapı tamamen sorted değildir.

```text
        2
      /   \
     5     4
    / \   /
   9   8  7
array = [2,5,4,9,8,7]
```

## Karmaşıklık
- peek: O(1)
- push/pop: O(log n)
- heapify: O(n)
- bounded Top-K: O(n log k), O(k) ek alan

## Interview patterns
Top-K, k-way merge, scheduler/event queue, running median (iki heap), Dijkstra frontier. Priority update/delete gereken uygulamalarda entry map + lazy deletion veya indexed heap düşünülebilir.

## Production trade-off'ları
Priority queue'yu unbounded bırakmak memory riskidir. Equal priorities için sequence/tie-breaker determinism sağlar. Stale entries lazy deletion kullanılıyorsa memory ve cleanup politikası gerekir. K küçükse bounded heap tüm dataset'i sort etmekten daha uygundur.

## Kaynak
- https://docs.python.org/3/library/heapq.html
