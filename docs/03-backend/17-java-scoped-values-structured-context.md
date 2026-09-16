# Java Scoped Values & Structured Request Context

## Problem
Request ID, principal ve tracing context gibi cross-cutting verileri her metoda explicit parametreyle geçirmek gürültü yaratır; global mutable state ise concurrency için güvenli değildir. `ThreadLocal` context propagation sağlar fakat pool reuse, cleanup ve unconstrained mutation sorunları doğurabilir. `ScopedValue`, bounded dynamic scope boyunca immutable binding paylaşmayı amaçlar.

```text
request entry
  -> ScopedValue.where(CONTEXT, value)
       -> service
       -> repository
       -> structured child tasks
  <- scope exits; binding disappears
```

## Mental model
Scoped value'yu global değişken olarak değil, call tree'ye bağlanmış read-mostly ambient parameter olarak düşün. Binding immutable'dır; nested scope aynı key'i yeniden bind edebilir. Structured task tree mevcut binding'leri kontrollü biçimde inherit edebilir.

## ThreadLocal ile fark
ThreadLocal'ın lifetime'ı thread'e bağlanabilir ve explicit cleanup gerektirebilir. ScopedValue lifetime'ı execution scope ile hizalamayı hedefler. Bu, özellikle virtual threads ve structured concurrency ile daha anlaşılır bir context ownership modeli sağlar.

Ancak ScopedValue içindeki nesne mutable ise thread safety otomatik gelmez. Shared mutable object eşzamanlı erişiliyorsa yine synchronization veya immutable data tasarımı gerekir.

## Mülakat soruları
- Dynamic scope ile lexical scope farkı nedir?
- ScopedValue hangi ThreadLocal failure mode'larını azaltır?
- Immutable binding ne kazandırır?
- Structured child task inheritance nasıl düşünülmelidir?
- Mutable payload neden hâlâ synchronization gerektirir?
- Tracing context için explicit parameter ile ambient context arasında nasıl seçim yaparsın?

## Seviye beklentisi
Junior: thread context ve scope. Mid: binding/lifetime. Senior: virtual threads, cleanup ve tracing. Staff: framework/API governance ve compatibility. Principal/CTO: concurrency standardı, migration maliyeti ve ecosystem readiness.

## Failure modes / production
Ambient context ile business dependency gizlemek, mutable payload'ı güvenli sanmak, scope dışı lifetime varsaymak, hedef JDK'nın API/preview durumunu kontrol etmemek ve tracing framework propagation'ını test etmemek başlıca risklerdir. Context-missing errors, trace continuity, cancellation latency ve migration regressions izlenmelidir.

## Alıştırma / proje
Request ID, principal ve deadline için explicit-vs-scoped kararını ver. Ardından ThreadLocal ve ScopedValue varyantlı bir HTTP fan-out servisi kur; exception, cancellation, nested rebind ve stale-context testleri çalıştır.

## Kaynaklar
- OpenJDK — JEP 506 Scoped Values: https://openjdk.org/jeps/506
- Java SE 25 API — ScopedValue: https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ScopedValue.html
- OpenJDK — Project Loom: https://openjdk.org/projects/loom/
