# Python asyncio TaskGroup, Cancellation & Structured Concurrency

## Konu anlatımı
Structured concurrency concurrent task yaşam sürelerini lexical scope'a bağlar. Python `asyncio.TaskGroup` child task ownership'ini açık hale getirir: group scope'u tamamlanmadan child'lar tamamlanır. İlk non-cancellation failure kalan sibling task'ları cancel eder; cleanup tamamlandıktan sonra hatalar gerektiğinde `ExceptionGroup` olarak raporlanır.

Cancellation cooperative'dir. `Task.cancel()` task'ı zorla öldürmek yerine uygun noktada `CancelledError` üretir. Resource cleanup `try/finally` içinde yapılmalı; `CancelledError` yakalanırsa cleanup sonrası genellikle yeniden yükseltilmelidir. `TaskGroup` ve `asyncio.timeout()` cancellation'ı kendi protokollerinin parçası olarak kullanır.

## Mental model
```text
scope
 +-- TaskGroup
     +-- A
     +-- B -- failure
     +-- C -- cancellation -> finally
          |
     collect children
          |
     ExceptionGroup
```

## Mülakat soruları
- Structured concurrency hangi ownership invariant'ını sağlar?
- Cancellation neden cooperative'dir?
- `CancelledError` neden swallow edilmemelidir?
- TaskGroup child failure'ı sibling'leri nasıl etkiler?
- Nested timeout/cancellation tasarımında deadline nasıl propagate edilir?

## Beklenen cevap seviyesi
Mid seviyede task/await/cancellation; Senior seviyede ownership, cleanup ve ExceptionGroup; Staff seviyede nested cancellation, deadline propagation, bounded cleanup ve orphan-task observability beklenir.

## Mini alıştırma
Üç upstream çağrıyı TaskGroup ile fan-out et; bir child fail olduğunda sibling cancellation ve cleanup akışını test et.

## Proje fikri
`structured-concurrency-lab`: `create_task`, `gather` ve `TaskGroup` sürümlerini failure/timeout injection ile karşılaştır.

## Failure modes / production
`CancelledError`'ı yutmak, fire-and-forget task kaybetmek, cleanup'ı sınırsız tutmak ve child I/O'ya deadline taşımamak başlıca risklerdir. Active task, cancellation reason, deadline exceeded ve orphan task sinyallerini izle.

## Kaynaklar
- https://docs.python.org/3.14/library/asyncio-task.html
- https://docs.python.org/3.14/library/asyncio-exceptions.html
