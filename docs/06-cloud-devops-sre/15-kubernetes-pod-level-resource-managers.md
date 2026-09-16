# Kubernetes Pod-Level Resource Managers, NUMA & Sidecar Economics

## Neden önemli?
Kubernetes v1.37'de `PodLevelResourceManagers` Beta'ya geçti (varsayılan kapalı). CPU Manager, Memory Manager ve Topology Manager Pod seviyesindeki `.spec.resources` bildirimlerini donanım yerleşiminde kullanabilir. Amaç latency-sensitive ana workload'a exclusive/NUMA-local kaynak verirken küçük sidecar'lara gereksiz dedicated core ayırmamaktır.

```text
Pod envelope
+----------------------------------+
| main -> exclusive CPU/memory     | -> NUMA local
| sidecar -> pod shared pool       | -> utilization
+----------------------------------+
```

## Mental model
Resource request yalnız scheduler kapasite hesabı değildir; node içinde placement ve isolation kararlarının girdisi olabilir. Pod-level resource managers bu kararı container sınırından Pod workload sınırına yükseltir.

## Mülakat ekseni
Junior: request/limit. Mid: Guaranteed QoS ve NUMA. Senior: CPU/Memory/Topology Manager ve noisy neighbor. Staff: node-pool rollout, feature gate, observability ve rollback. Principal/CTO: utilization-tail latency ekonomisi.

## Failure modes ve trade-off
- Feature gate'i geniş blast radius ile açmak.
- Pod ve container resource semantics'ini karıştırmak.
- Sidecar contention'ı ölçmemek.
- NUMA locality gerektirmeyen workload'a gereksiz complexity eklemek.
- Ortalama latency ile yetinip p99 regression'ı kaçırmak.

## Production bağlantısı
Inference, low-latency JVM/C++ servisleri, network processing ve telemetry sidecar'lı CPU-sensitive workload'larda değerlidir. CPU pinning, NUMA locality, throttling, memory pressure, p99 latency ve fleet utilization birlikte izlenmelidir.

## Alıştırma / proje
8 CPU isteyen inference container ve telemetry sidecar için exclusive/shared placement tasarla. `pod-resource-manager-lab` ile feature gate açık/kapalı benchmark üret.

## Kaynaklar
- https://kubernetes.io/blog/2026/09/15/kubernetes-v1-37-pod-level-resource-managers-beta/
- https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/
