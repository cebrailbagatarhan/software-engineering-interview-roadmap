# Kubernetes HPA Scale-to-Zero: Queueing, Cold Starts & Cost/SLO Trade-offs

Kubernetes v1.37 ile HorizontalPodAutoscaler'ın uygun object veya external metric kullanan workload'ları sıfır replica'ya indirebilmesi Beta ve varsayılan açık hale geldi. Bu özellikle queue consumer, batch worker ve pahalı CPU/GPU kaynaklarını idle durumda tutmak istemeyen sistemler için önemlidir.

## Mental model

```text
producer -> durable queue -> demand metric -> HPA -> replicas 0..N
                                      |                |
                                      +------ cold-start path
```

Scale-to-zero'nun temel bedeli cold start'tır. Talep geldiğinde metric pipeline'ın bunu görmesi, HPA'nın reconcile etmesi, scheduler'ın Pod yerleştirmesi, gerekirse image'ın çekilmesi, runtime/application init ve readiness tamamlanmalıdır. Queue backlog bu gecikmeyi absorbe edebilir; Kubernetes Service ise sıfır ready endpoint varken HTTP request'lerini buffer etmez.

## Metric seçimi
CPU gibi Pod'a bağlı bir metric replicas=0 iken talebi ifade edemez. Queue depth, oldest-message-age veya başka bir external/object metric talep sinyalini compute'tan bağımsız tutar. Depth throughput ihtiyacını, oldest age ise kullanıcıya görünen bekleme riskini daha iyi gösterebilir.

## Interview checkpoints
- Scale-from-zero için metric neden workload dışından gözlenebilmelidir?
- Queue depth ile queue age hangi farklı failure mode'ları gösterir?
- HTTP request-driven sistemde hangi buffering katmanı gerekir?
- Cold-start budget nasıl parçalanır?
- GPU worker'da minReplicas=0 ile warm capacity arasındaki ekonomik trade-off nedir?

## Production failure modes
Stale external metric, image-pull latency, scheduler capacity shortage, burst'te overshoot, scale-down sırasında in-flight job kaybı ve poison-message retry storm kritik risklerdir. Backlog age/depth, zero-to-ready süresi, scheduling ve image-pull latency, retry rate, completion p95/p99 ve idle compute cost birlikte izlenmelidir.

## Kaynaklar
- https://kubernetes.io/blog/2026/09/02/kubernetes-v1-37-hpa-scale-to-zero-beta/
- https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
