# Kubernetes Dynamic Resource Allocation (DRA)

## Neden var?
GPU, NIC ve FPGA gibi cihazları yalnız integer extended resource olarak modellemek heterogeneous accelerator filolarında seçim, paylaşım, health ve lifecycle ihtiyaçlarını karşılamaz. Dynamic Resource Allocation (DRA), cihaz talebini storage dünyasındaki dynamic provisioning'e benzer biçimde declarative hale getirir.

```text
Workload -> ResourceClaim -> DeviceClass/selectors -> Scheduler -> Node/DRA driver -> Device
```

Kubernetes'in çekirdek DRA mekanizması v1.35'ten beri Stable. v1.37'de DRA Extended Resource desteği GA olarak mevcut workload'ların `example.com/gpu` biçimini koruyup allocation backend'ini DRA'ya taşıyabilmesini sağlar. Device taints/tolerations da v1.37'de Stable'dır.

## Mental model
- `DeviceClass`: platformun cihaz seçimi/policy yüzeyi.
- `ResourceClaim`: workload'un allocation isteği ve lifecycle kaydı.
- Scheduler: claim ile uygun cihaz/node eşleşmesini koordine eder.
- DRA driver: node tarafında cihazı hazırlar ve lifecycle operasyonlarını yürütür.

DRA'yı yalnız yeni bir GPU API'si değil, scarce/specialized hardware için scheduling-time resource negotiation katmanı olarak düşün.

## Mülakat derinliği
Junior seviyesinde request/scheduling/device ayrımını; Mid seviyede DeviceClass/ResourceClaim lifecycle'ını; Senior seviyede fragmentation, health, quota ve failure modes'u; Staff seviyesinde heterogeneous fleet, migration ve tenancy governance'ını; Principal/CTO seviyesinde accelerator utilization, portability ve capacity economics'i açıklayabilmelisin.

## Kritik sorular
1. DRA klasik extended resource modelinden hangi açılardan daha zengindir?
2. DeviceClass ile ResourceClaim sorumlulukları nasıl ayrılır?
3. DRA ile PVC/StorageClass modeli nerede benzer?
4. Extended Resource GA brownfield migration'ı neden kolaylaştırır?
5. Device taints hangi production riskini azaltır?
6. Multi-tenant GPU platformunda DRA, quota ve queueing nasıl birlikte çalışır?

## Failure modes ve trade-off
DeviceClass'a application-specific policy yığmak, scarce device için quota/admission katmanını unutmamak, driver failure ile scheduler failure'ı karıştırmak, unhealthy cihazları yeni workload'a vermek, claim leak ve iki migration modelinin observability'sini ayırmamak başlıca risklerdir.

Production'da allocation latency, pending reason, device utilization/fragmentation, claim leak, driver errors, unhealthy/tainted device ve queue wait izlenmelidir.

## Mini alıştırma / proje
A100, H100 ve iki NIC sınıfı için training, inference ve batch workload'larını modelle. Ardından fake DRA driver ile claim allocation, unavailable device, taint ve extended-resource compatibility testleri kur.

## Kaynaklar
- Kubernetes Docs — Dynamic Resource Allocation: https://kubernetes.io/docs/concepts/resource-management/dynamic-resource-allocation/
- Kubernetes v1.37 DRA Updates — 3 Eylül 2026: https://kubernetes.io/blog/2026/09/03/kubernetes-v1-37-dra-updates/
- Kubernetes v1.36 Release: https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/
