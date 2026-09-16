# Kubernetes Memory QoS, cgroup v2 & Reclaim Economics

## Neden önemli?
Kubernetes v1.37'de Memory QoS Beta ve feature gate varsayılan açık. Bu, policy'nin otomatik aktif olduğu anlamına gelmez: varsayılan kubelet config memory throttling/reservation uygulamaz.

## Mental model
`memory.min` hard protection, `memory.low` best-effort protection, `memory.high` ise reclaim/throttling pressure boundary olarak düşünülebilir. Protection arttıkça kernel'in reclaim özgürlüğü azalır; bu nedenle latency-sensitive workload korunurken komşu workload'ların riskini artırmak mümkündür.

```text
pressure -> cgroup v2 -> min / low / high
                       |      |      |
                     hard   soft   throttle
```

## Production trade-off'ları
Tiered reservation Guaranteed pod'lara `memory.min`, Burstable pod'lara `memory.low` uygulayabilir. Policy node-wide olduğundan heterojen workload'larda node-pool segmentation gerekebilir. Page cache cgroup'a charge edildiği için file-heavy workload protected memory'yi büyütebilir.

İzlenecek sinyaller: working set, RSS/cache breakdown, PSI, reclaim, OOM, throttling, p95/p99 latency ve allocatable headroom.

## Mülakat ekseni
Senior aday cgroup v2 reclaim ve tail latency'yi; Staff aday mixed workload placement ve rollout'u; Principal/CTO utilization-reliability-cloud-cost dengesini açıklayabilmelidir.

## Kaynaklar
- https://kubernetes.io/blog/2026/09/14/kubernetes-v1-37-memory-qos-graduates-to-beta/
- https://kubernetes.io/docs/concepts/architecture/cgroups/
- https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
