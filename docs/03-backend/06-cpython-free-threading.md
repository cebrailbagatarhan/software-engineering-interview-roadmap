# CPython Free-Threading, GIL & Thread Safety

## Mental model
```text
Classic: threads -> GIL -> interpreter
Free-threaded: threads -> concurrent execution -> explicit shared-state safety
```

CPython'ın klasik build'inde GIL Python bytecode execution'ını büyük ölçüde serialize eder. PEP 703 opsiyonel GIL yolunu tanımlar; Python 3.14 free-threading Phase II/supported aşamasındadır. Bu değişim CPU-bound thread'ler için paralellik fırsatı açar fakat application-level synchronization ihtiyacını kaldırmaz. Third-party C extension compatibility, single-thread overhead ve shared-state contention production migration'ın ana trade-off'larıdır.

## Mülakat odağı
- GIL neyi korur, neyi korumaz?
- I/O concurrency ile CPU parallelism ayrımı.
- Free-threaded build'de race condition ve lock tasarımı.
- Process pool vs thread vs free-threaded runtime.
- Dependency compatibility ve rollback planı.

## Mini alıştırma
CPU-bound serviste classic threads, process pool ve free-threaded build'i throughput, RSS ve isolation açısından benchmark et.

## Failure modes / production
Extension compatibility'yi atlamak; GIL'i application lock sanmak; microbenchmark'a aşırı güvenmek; single-thread regression ve memory davranışını ölçmemek.

## Kaynaklar
- https://peps.python.org/pep-0703/
- https://peps.python.org/pep-0779/
- https://docs.python.org/3/howto/free-threading-python.html
