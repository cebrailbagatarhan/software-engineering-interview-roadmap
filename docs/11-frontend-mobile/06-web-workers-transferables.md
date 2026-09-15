# Web Workers, Structured Clone & Transferable Objects

## Konu anlatımı
Web Workers CPU-ağır JavaScript işini UI execution context'inden ayırabilir. `postMessage()` veriyi structured clone algoritmasıyla taşır; page ve worker çoğunlukla aynı object instance'ını paylaşmaz. Büyük payload'larda clone maliyeti önemlidir.

`ArrayBuffer` gibi transferable kaynaklar ownership transfer ile hedef context'e taşınabilir; gönderen buffer detached olur. Function ve DOM node gibi değerler structured-cloneable değildir ve `DataCloneError` üretebilir. Worker kullanımı otomatik hızlanma değildir: task granularity, startup/message overhead ve CPU contention ölçülmelidir.

## Mental model
```text
Main thread -- structured clone --> Worker
Main thread <-- structured clone -- Worker

ArrayBuffer owner A -- transfer --> owner B
owner A buffer = detached
```

## Mülakat soruları
- Worker neyi çözer?
- Structured clone nasıl çalışır?
- Transferable neden büyük binary payload için yararlıdır?
- Transfer sonrası sender buffer'a ne olur?
- Worker pool/backpressure nasıl tasarlanır?

## Beklenen cevap seviyesi
Mid: worker/postMessage. Senior: clone/transfer/overhead/cancellation. Staff: pool sizing, observability, fallback ve responsiveness SLO.

## Mini alıştırma
50 MB ArrayBuffer için clone ve transfer akışlarını karşılaştır.

## Proje fikri
`worker-transfer-lab`: main-thread, worker+clone ve worker+transfer performansını ölç.

## Production bağlantısı ve failure modes
Her işi worker'a atmak; büyük buffer'ları sürekli clone etmek; detached buffer'ı tekrar kullanmak; cancellation/error protokolü olmaması; aşırı worker ile contention.

## Kaynaklar
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Transferable_objects
