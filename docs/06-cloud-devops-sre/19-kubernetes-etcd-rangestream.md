# Kubernetes etcd RangeStream: Large LIST Reads ve Memory Amplification

## Neden önemli?
Kubernetes API server watch cache'i başlatırken veya yeniden kurarken etcd'den büyük resource collection'ları okuyabilir. Kubernetes v1.37 + etcd v3.7 RangeStream, bu büyük okumaların peak memory maliyetini daha öngörülebilir hale getirmeyi hedefler.

## Mental model
```text
Unary: etcd [full page] -> apiserver [full page] -> decode
Stream: etcd [chunk] -> apiserver [chunk] -> incremental decode
```
Key-count pagination byte-count bound değildir. Object-size skew varsa bir page'in byte boyutu dramatik değişebilir.

## Internals ve trade-off
Unary Range response page'i sender tarafında materialize eder; receiver decode sırasında aynı payload'ı da tutabilir. Streaming daha küçük bounded buffers ve backpressure ile peak RSS'i düşürebilir. Karşılığında stream lifecycle, flow control ve partial-progress handling karmaşıklığı gelir.

## Mülakat derinliği
Junior LIST/WATCH ve pagination'ı; Mid buffer/streaming'i; Senior memory amplification/backpressure/cache re-init'i; Staff CRD size governance ve fleet capacity'yi; CTO reliability economics ve platform guardrail'lerini tartışmalıdır.

## Failure modes
- Average object size ile kapasite planlamak
- Consumer backpressure'ı yok saymak
- CRD payload büyümesini sınırlamamak
- Cache re-init senaryosunu load test etmemek

## Production bağlantısı
API server ve etcd RSS/GC, LIST latency, bytes/read, object-size histogram, watch-cache initialization time, restart/OOM ve concurrent large-read sayısı izlenmelidir.

## Kaynaklar
- https://kubernetes.io/blog/2026/09/01/kubernetes-v1-37-etcd-range-stream/
- https://etcd.io/docs/v3.7/
- https://kubernetes.io/docs/reference/using-api/api-concepts/
