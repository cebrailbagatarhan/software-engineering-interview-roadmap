# Kubernetes HPA: Control Loop, Stabilization & Thrashing

## Mental model
HPA bir feedback controller'dır: observed metric'i target ile karşılaştırıp desired replica sayısını hesaplar. Gerçek davranış metric delay, pod startup/readiness, policy ve downstream capacity ile oluşur.

```text
traffic -> pods -> metric
           ^        |
           |        v
        replicas <- HPA controller
```

`autoscaling/v2` behavior ile scale-up/down policy, stabilization window ve tolerance ayarlanabilir. Stabilization flapping'i azaltır; capacity yaratmaz. Node yoksa pod Pending kalır, DB/downstream dar boğazsa replica artırmak overload'u büyütebilir.

## Interview depth
Mid: target -> desired replicas. Senior: readiness, startup, stabilization, external metrics. Staff: node autoscaling, SLO, cost, capacity ceilings ve failure containment.

## Production failure modes
Noisy metric thrashing, startup süresini yok saymak, Pending pod'u capacity sanmak, downstream quota'yı hesaba katmamak ve min/max replica'yı load test olmadan seçmek.

## Kaynak
- https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
