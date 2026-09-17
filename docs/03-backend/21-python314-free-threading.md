# Python 3.14 Free-Threading: GIL, Parallelism & Migration

## Mental model
Klasik CPython'da GIL Python bytecode execution'ını aynı process içinde büyük ölçüde seri hale getirir. Python 3.14'te free-threaded build resmi desteklenen opsiyonel moddur: thread'ler Python kodunu gerçekten paralel çalıştırabilir, fakat shared-state synchronization ve native-extension compatibility daha görünür maliyet olur.

```text
classic: T1 ----run---- wait ----run
         T2 ....wait... run .....wait

free:    T1 ----run---------run----
         T2 ----run--lock?--run----
```

## Mülakat omurgası
- CPU-bound ve I/O-bound workload'u ayır.
- GIL'in race-condition safety garantisi olmadığını belirt.
- Free-threading'de speedup'ın core, serial fraction ve contention ile sınırlı olduğunu açıkla.
- C extensions/wheels için compatibility inventory ve canary benchmark öner.
- Alternatifleri karşılaştır: async I/O, threads, multiprocessing, multiple interpreters.

## Production trade-off
Throughput/core artabilir; buna karşılık lock contention, RSS, native dependency uyumsuzluğu ve tail latency regression riski vardır. Fleet migration'da throughput, p95/p99, CPU, RSS, context switches ve extension compatibility izlenmelidir.

## Alıştırma
%80 paralelleşebilir workload için 8 thread Amdahl üst sınırını hesapla ve gerçek sonucun neden daha düşük olacağını tartış.

## Proje
Classic/free-threaded/multiprocessing modlarını 1/2/4/8 worker ile benchmark eden harness kur; dependency compatibility matrisi ekle.

## Kaynaklar
- https://www.python.org/downloads/release/python-3147/
- https://peps.python.org/pep-0779/
- https://docs.python.org/3/howto/free-threading-extensions.html
