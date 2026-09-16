# Python Free-Threading: GIL Boundaries & Migration

Python 3.14 ile free-threaded CPython resmi olarak desteklenen fakat opsiyonel bir build moduna geçti. GIL devre dışıyken CPU-bound Python thread'leri birden fazla core üzerinde paralel ilerleyebilir; ancak bu otomatik hızlanma veya otomatik thread safety anlamına gelmez.

```text
GIL build:       T1/T2 -> [GIL] -> one Python executor
free-threaded:   T1 -> core1
                 T2 -> core2
                   \-> shared state: locks/atomics
```

## Temel mental model
GIL'in kalkması gizli global serialization'ın kalkmasıdır. Shared mutable state için açık synchronization ihtiyacı daha görünür hale gelir. Lock contention, allocator/GC overhead ve third-party C extension davranışı throughput'u belirleyebilir. Bazı extension'lar GIL'i yeniden etkinleştirebilir.

## Migration sırası
1. CPU-vs-I/O workload'u profile et.
2. Dependency ve C-extension compatibility matrix çıkar.
3. Race/correctness stress tests çalıştır.
4. Normal vs free-threaded build benchmark et.
5. Canary rollout ile p99, throughput/core, CPU/RSS ve errors izle.
6. Geri dönüş yolunu hazır tut.

## Mülakat ekseni
GIL neyi serialize eder? CPU-bound ve I/O-bound workload neden farklı etkilenir? C extension GIL'i yeniden açarsa ne olur? Lock granularity nasıl seçilir? Staff seviyesinde dependency ecosystem ve rollout riski nasıl yönetilir?

## Production failure modes
Free-threading'i 'lock gereksiz' diye yorumlamak, microbenchmark'a aşırı güvenmek, extension compatibility'yi atlamak ve shared mutable cache'leri korumasız bırakmak başlıca risklerdir.

## Kaynaklar
- https://docs.python.org/3/whatsnew/3.14.html
- https://peps.python.org/pep-0779/
- https://docs.python.org/3/howto/free-threading-python.html
