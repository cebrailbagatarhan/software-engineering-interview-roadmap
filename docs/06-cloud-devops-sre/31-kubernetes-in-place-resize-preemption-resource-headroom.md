# Kubernetes In-Place Pod Resize Preemption & Resource Headroom

## Konu anlatımı
Kubernetes'te in-place vertical scaling, çalışan Pod'u recreate etmeden container CPU/memory request ve limit'lerini değiştirmeyi sağlar; core özellik v1.35'ten beri stable. Scale-up node headroom'unu aştığında kubelet request'i geçerli fakat geçici olarak uygulanamaz anlamında `Deferred` bırakabilir. Kubernetes v1.37'de opt-in Alpha `InPlacePodVerticalScalingSchedulerPreemption`, scheduler'ın aynı node'daki lower-priority Pod'ları preempt ederek bu resize için kapasite açabilmesini ekledi.

Normal scheduling preemption yeni Pod'a node arar; resize preemption'da Pod zaten node'a bağlıdır ve victim search yalnız o node'dadır. Scheduler requested delta'yı reservation olarak hesaba katar; kubelet ise CRI/cgroup actuation yapar. `resizePolicy` resource bazında restart gereksinimini tanımlar. QoS class creation-time'da sabittir ve resize ile değişmez.

## Mental model
```mermaid
flowchart LR
  V[VPA/operator] --> R[/resize]
  R --> K[Kubelet]
  K -->|capacity| C[CRI/cgroup update]
  K -->|no capacity| D[Deferred]
  D --> S[Scheduler]
  S -->|same node| P[Preempt lower priority]
  P --> K
```

## İçeride ne oluyor?
- `/resize` subresource desired CPU/memory'i değiştirir.
- Kubelet `PodResizePending` / `PodResizeInProgress` ile progress bildirir.
- `Deferred` temporary capacity problemidir; `Infeasible` constraint nedeniyle uygulanamaz request'tir.
- v1.37 Alpha scheduler preemption same-node victim seçebilir.
- CPU ve memory resize'ın runtime riskleri farklıdır; memory downsize best-effort ve race-prone olabilir.
- PDB, PriorityClass ve graceful termination operasyonel sonucu etkiler.

## Mülakat soruları
1. Horizontal ve vertical scaling neyi farklı çözer?
2. Deferred ve Infeasible farkı nedir?
3. Resize preemption neden same-node'dur?
4. Memory resize neden CPU resize'dan daha risklidir?
5. PDB ve PriorityClass nasıl devreye girer?
6. Staff: headroom ile bin-packing ekonomisini nasıl dengelersin?
7. Principal: VPA, scheduler preemption ve Cluster Autoscaler feedback loop'unu nasıl yönetirsin?

## Beklenen cevap seviyesi
- **Mid:** request/limit, resizePolicy ve status semantics.
- **Senior:** kubelet/scheduler rolleri, PDB, memory riskleri.
- **Staff:** capacity headroom, priority taxonomy ve SLO.
- **Principal:** fleet economics ve autoscaling governance.

## Mini alıştırma
8 CPU node'da 4 CPU high-priority + 3 CPU low-priority Pod varken high-priority Pod'u 6 CPU'ya resize et. Deferred → victim → completed zincirini ve PDB engelini tartış.

## Proje fikri
`k8s-resize-preemption-lab`: PriorityClass, `/resize`, event collector ve latency/headroom dashboard'u. Resize wait, victim count, restart ve application latency ölç.

## Failure modes / trade-off / production bağlantısı
Resize'ın anında uygulanacağını varsaymak, aggressive memory downsize, priority inflation, preemption-proof low-priority workload ve autoscaler feedback loop'larını yok saymak tipik hatalardır. Resize pending duration, Deferred/Infeasible, victim count, restart, node headroom, OOM ve SLO latency izlenir.

## Kaynaklar
- Kubernetes v1.37 — Scheduler Preemption for In-Place Pod Resize, 10 Eylül 2026: https://kubernetes.io/blog/2026/09/10/kubernetes-v1-37-scheduler-preemption-for-in-place-pod-resize-alpha/
- Kubernetes — Resize CPU and Memory Resources assigned to Containers: https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/
- Kubernetes — Resource Management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
