# Kubernetes PodDisruptionBudget, Eviction & Safe Drain

PodDisruptionBudget voluntary disruption sırasında bir workload'da eşzamanlı unavailable replica miktarını `minAvailable` veya `maxUnavailable` ile sınırlar. Eviction API ve `kubectl drain` PDB'yi dikkate alır. PDB node crash gibi involuntary disruption'ı engellemez ve tek başına HA garantisi değildir.

## Mental model
```text
replicas=5, minAvailable=4
[P][P][P][P][P] --evict--> at most one voluntary unavailable

PDB = voluntary disruption budget
PDB != node-failure prevention
```

## Mülakat odağı
- Voluntary/involuntary disruption ayrımı.
- `minAvailable` vs `maxUnavailable`.
- PDB ile Deployment rollout kontrolünün farkı.
- Çok katı PDB'nin maintenance'i bloklaması.
- Quorum workload'larda application semantics ve failure domain.

## Production
PDB'yi readiness, termination grace, rollout strategy, topology/failure domains ve maintenance automation ile birlikte tasarla. Blocked eviction ve drain duration için telemetry/alerting ekle.

## Kaynaklar
- https://kubernetes.io/docs/tasks/run-application/configure-pdb/
- https://kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/
- https://kubernetes.io/docs/reference/kubernetes-api/policy-resources/pod-disruption-budget-v1/
