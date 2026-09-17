# WASI 0.3 Native Async, Component Boundaries & Portable Services

## Temel fikir
WebAssembly Component Model typed interfaces ve composition sağlar. WASI 0.3, 11 Haziran 2026'da ratify edildi ve `async func`, `stream<T>` ve `future<T>` primitives'lerini Canonical ABI seviyesine taşıdı.

## Mental model
```text
component A -- async WIT --> Canonical ABI --> host scheduler --> component B
                         stream / future
```

Async'in contract'ın parçası olması farklı language runtime'larının readiness ve backpressure ilişkisini host üzerinden compose etmeyi kolaylaştırır.

## Interface tasarımı
`future<T>` tek bir gelecekteki sonucu, `stream<T>` ise zaman içinde akan değerleri modellemek için uygundur. Interface yalnız type correctness değil cancellation, buffering ve backpressure davranışını da düşünmelidir.

## Mülakat derinliği
- Mid: core module, component ve WIT farklarını açıkla.
- Senior: async ABI, backpressure, cancellation ve WIT/toolchain pinning'i tartış.
- Staff: component boundary ile container/microservice boundary'yi karşılaştır.
- CTO: portability kazanımını runtime maturity, ecosystem ve organizational skill maliyetiyle değerlendir.

## Failure modes
WASI 0.2/0.3 mismatch, WIT pin drift, unbounded buffering, cancellation propagation eksikliği, runtime-specific assumptions ve Wasm'i container'ların evrensel yerine koymak.

## Production bağlantısı
Queue depth, stream throughput, cancellation latency, component instantiation errors, version mismatch, host CPU/RSS ve cold-start ölçülmelidir.

## Kaynaklar
- https://bytecodealliance.org/articles/WASI-0.3
- https://component-model.bytecodealliance.org/reference/faq.html
- https://component-model.bytecodealliance.org/running-components/wasmtime.html
