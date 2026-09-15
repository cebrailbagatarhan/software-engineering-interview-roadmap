# Web Locks API: Multi-Tab Coordination ve Deadlock Discipline

## Problem
Aynı origin'in birden fazla tab veya worker instance'ı IndexedDB sync, token refresh veya cache migration gibi logical resource'larda duplicate/concurrent work üretebilir. Tek bir JavaScript event loop yalnız kendi execution context'i için geçerlidir; tab'lar arası mutual exclusion sağlamaz.

## Mental model
```text
Tab A ---+
Tab B ---+--> request("resource") -> queue -> owner -> async work -> release
Worker --+

scope: same origin/browser coordination
NOT: server/global distributed lock
```

## API modeli
`navigator.locks.request(name, callback)` isimlendirilmiş lock'u asynchronous olarak ister. Callback tamamlandığında lock bırakılır. Varsayılan `exclusive`; uygun use case'te `shared` mode seçilebilir. Web Locks secure context gerektirir ve worker context'lerinde de kullanılabilir. `LockManager.query()` held/pending lock'ları diagnostic olarak gösterebilir.

## Deadlock
Bir tab A lock'unu tutup B'yi, başka tab B'yi tutup A'yı beklerse progress durur. Nested acquisition'dan kaçınmak, global ordering uygulamak ve bounded cancellation/timeout yaklaşımı kullanmak temel savunmalardır.

## Interview soruları
- Multi-tab race neden tek-threaded JS ile çözülmez?
- Exclusive/shared lock farkı nedir?
- Leader election pattern'i nasıl kurulur?
- Web Locks neden distributed lock değildir?
- IndexedDB transaction ile Web Lock hangi farklı scope'ları korur?
- İki named lock ile deadlock nasıl önlenir?

## Seviyeye göre cevap
Mid named resource ve exclusive access'i açıklar. Senior queueing, lock scope, deadlock ve cancellation'ı bağlar. Staff browser lifecycle, crash/reload, server idempotency ve observability ile end-to-end tasarım yapar.

## Mini alıştırma
Üç tab aynı anda auth refresh isterken `auth-refresh` lock'u ile single-flight akışı tasarla. Bekleyen tab'ların güncel token'ı nasıl gözlemleyeceğini ve server idempotency'nin neden hâlâ gerekli olduğunu açıkla.

## Proje
İki tab ve bir worker ile IndexedDB sync lab'i kur. Lock açık/kapalı duplicate work, acquisition wait ve hold duration ölç. A→B / B→A nested-lock deadlock demonstrasyonu ekle.

## Failure modes / production
Lock callback'inde uzun I/O, undefined lock ordering, server-side idempotency'yi kaldırmak ve Web Lock'u cross-device mutex sanmak önemli hatalardır. Production telemetry'de acquisition wait, hold duration, duplicate sync ve refresh failures izlenmelidir.

## Kaynaklar
- https://w3c.github.io/web-locks/
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API
- https://developer.mozilla.org/en-US/docs/Web/API/LockManager
