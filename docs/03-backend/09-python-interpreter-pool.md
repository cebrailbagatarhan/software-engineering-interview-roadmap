# Python InterpreterPoolExecutor & Subinterpreters

## Konu anlatımı
Python 3.14 `InterpreterPoolExecutor`, worker başına ayrı interpreter ve GIL kullanarak aynı process içinde CPU-bound Python işinde multi-core parallelism sağlayabilir. İzolasyon nedeniyle mutable Python state ve module runtime state normal thread modeli gibi paylaşılmaz; serialization ve native-extension uyumluluğu tasarımın parçasıdır.

## Mental model
```text
process
 |-- thread -> interpreter A -> GIL A -> core 1
 `-- thread -> interpreter B -> GIL B -> core 2
```

## Mülakat soruları
- Thread, interpreter ve process pool ne zaman seçilir?
- Ayrı GIL neden gerçek CPU parallelism sağlar?
- Isolation ve serialization hangi maliyetleri getirir?
- Native extension compatibility nasıl doğrulanır?

## Beklenen cevap seviyesi
Mid temel concurrency ayrımını; Senior isolation/serialization/benchmark'ı; Staff compatibility, rollout ve fallback stratejisini bağlamalıdır.

## Mini alıştırma
Aynı CPU-bound işi üç executor ile 1/2/4 worker'da benchmark et.

## Proje fikri
`python-parallelism-lab`: throughput, p95, RSS ve startup maliyetini ölç.

## Production bağlantısı
Task granularity, C-extension desteği, crash isolation ve memory footprint benchmark edilmeden executor standardı seçilmemelidir.

## Kaynaklar
- https://docs.python.org/3.14/library/concurrent.futures.html#interpreterpoolexecutor
- https://docs.python.org/3.14/library/concurrent.interpreters.html
- https://docs.python.org/3.14/c-api/subinterpreters.html
