# Kubernetes DRA, GPU Allocation & Scheduler Scalability

## Neden önemli?
Accelerator scheduling yalnız GPU sayısı değildir. Device topology, memory/capacity, sharing, NUMA/PCIe locality, health ve tenant fairness placement kalitesini belirler.

Kubernetes 1.37'de DRA Extended Resource desteği GA oldu. DRA driver'ları geleneksel extended-resource isteklerini karşılayabilir; workload her durumda ayrı `ResourceClaim` yazmak zorunda değildir. Aynı release'teki PreQueueingHint çalışması ResourceClaim event'lerinde tüm unschedulable pod'ları yeniden taramak yerine ilgili pod'ları index ile hedefleyerek event amplification'ı azaltmayı amaçlar.

## Mental model
```text
Pod resource need
       |
 scheduler + DRA
       |
 DeviceClass / claims / capacity
       |
 node + device selection
       |
 node-side driver
       |
 prepare / expose device

claim event -> affected-pod index -> targeted requeue
```

Control-plane açısından temel risk event amplification'dır: tek device-state değişimi binlerce pending pod'u gereksiz yeniden değerlendirmeye iterse scheduler CPU'su gerçek placement işinden uzaklaşır.

## Mülakat derinliği
- Junior: resource request ve device resource.
- Mid: scheduling ve device plugin.
- Senior: topology, fragmentation, claims, recovery.
- Staff: scheduler scalability, fairness, fleet utilization.
- Principal/CTO: accelerator economics, portability, capacity strategy.

## Yüksek getirili sorular
1. Device Plugin ile DRA abstraction farkı nedir?
2. Extended Resource GA migration'ı nasıl kolaylaştırır?
3. GPU count neden yeterli scheduling sinyali değildir?
4. ResourceClaim hangi problemi çözer?
5. Event amplification scheduler throughput'u nasıl etkiler?
6. GPU fragmentation nasıl ölçülür ve azaltılır?
7. Fairness ile utilization nasıl dengelenir?

## Production failure modes
Topology'yi yok saymak; stale device health; claim lifecycle leak; büyük requeue storm; utilization uğruna starvation; allocation failure'larını yalnız pod-level hata olarak görmek.

İzlenecek sinyaller: pending duration, scheduling attempts, device utilization, fragmentation, allocation failures, claim lifecycle ve control-plane CPU.

## Alıştırma
8 GPU'lu iki node üzerinde 1/2/4-GPU workload'ları ve aynı high-speed interconnect grubunu isteyen 2-GPU işleri yerleştir. First-fit ile topology-aware placement'ın fragmentation farkını göster.

## Proje
`dra-scheduler-lab`: device inventory/topology modelle; naive first-fit ile topology/fairness-aware scorer'ı pending time, utilization, fragmentation ve scheduling attempts üzerinden karşılaştır.

## Kaynaklar
- https://kubernetes.io/blog/2026/09/03/kubernetes-v1-37-dra-updates/
- https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/
- https://kubernetes.io/releases/1.37/
