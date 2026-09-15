# Kubernetes Lease, Leader Election & Fencing

## Konu anlatımı
Leader election, replicated controller/worker grubunda belirli side-effect'leri tek aktif actor'a vermek için kullanılır. Kubernetes `coordination.k8s.io/v1` Lease nesnelerini node heartbeat ve component leader election dahil coordination ihtiyaçlarında kullanır.

Lease akışı acquire → renew → expire → takeover olarak düşünülebilir. `holderIdentity`, `renewTime` ve `leaseDurationSeconds` mevcut leadership durumunu taşır. Adaylar Kubernetes object `resourceVersion` üzerinden optimistic concurrency ile yarışır.

## Mental model
```text
A ---- CAS ----> Lease <---- CAS ---- B
                 holder=A
                    |
                 expire
                    v
                 holder=B

Election != fencing
old A -- epoch 41 --> storage REJECT
new B -- epoch 42 --> storage ACCEPT
```

## Kritik ayrım: election ve fencing
Election yeni leader'ı seçer; eski leader'ın external side-effect üretmesini otomatik olarak engellemez. Network partition veya uzun pause sonrası stale leader hâlâ database/queue'a erişebiliyorsa split-brain side-effect mümkündür. External resource destekliyorsa monoton epoch/fencing token stale write'ları reddetmelidir. Aksi durumda idempotency, version/ownership checks ve domain-specific guard gerekir.

## Mülakat soruları
- Lease ile mutex farkı nedir?
- Optimistic concurrency acquisition yarışını nasıl çözer?
- Leader election neden exactly-once değildir?
- GC pause stale leader riskini nasıl üretir?
- Lease timeout'ları availability/churn dengesini nasıl etkiler?
- Staff: storage fencing desteklemiyorsa hangi guard'ları kurarsın?

## Seviyeye göre cevap derinliği
Mid: leader/follower ve expiration. Senior: CAS, renew deadline, jitter ve failover. Staff: fencing, stale leader, external side effects ve control-plane outage. Principal: ortak coordination standardı, blast radius ve observability.

## Mini alıştırma
3 billing worker'da leader 8 saniye pause yaşarken lease expire olsun. Yeni leader seçildikten sonra eski leader'ın duplicate charge üretmesini epoch veya idempotency ile engelleyen akışı çiz.

## Proje fikri
`lease-fencing-lab`: üç Kubernetes worker + Lease + PostgreSQL epoch check. Pause, API timeout ve leader kill fault injection altında duplicate side-effect ve failover latency ölç.

## Production failure modes / trade-off
Election'ı fencing sanmak; leader-only işi idempotent yapmamak; timeout'u gerçek jitter/pause dağılımından bağımsız seçmek; API-server outage davranışını tanımlamamak. Leadership transition, renew failure/latency, stale-epoch rejection ve duplicate-side-effect metriği izlenmelidir.

## Kaynaklar
- https://kubernetes.io/docs/concepts/architecture/leases/
- https://kubernetes.io/docs/reference/kubernetes-api/coordination/lease-v1/
- https://kubernetes.io/docs/concepts/cluster-administration/coordinated-leader-election/
