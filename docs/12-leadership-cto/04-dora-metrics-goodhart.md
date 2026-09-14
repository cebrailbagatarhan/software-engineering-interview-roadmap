# DORA Metrics, Goodhart's Law & Delivery System Design

DORA'nın güncel software-delivery modeli throughput ve instability'yi birlikte ele alır. Beş sinyal: change lead time, deployment frequency, failed deployment recovery time, change fail rate ve deployment rework rate. Bunlar hedef puan değil, delivery system hakkında feedback sinyalidir.

```text
Capabilities -> delivery system -> DORA signals -> diagnose bottleneck
     ^                                      |
     +--------- experiment / learning ------+
```

Metric hedefe dönüştüğünde gaming riski oluşur: deployment frequency kotası anlamsız deploy'ları, sıfır fail-rate hedefi risk saklamayı teşvik edebilir. EM/CTO seviyesinde amaç ham skoru yükseltmek değil; batch size, CI, flaky tests, approvals, deploy automation, architecture coupling, observability ve recovery gibi capability bottleneck'lerini bulmaktır. DORA sinyalleri product outcome ve reliability/SLO ile birlikte yorumlanmalıdır.

## Interview checkpoints
- Güncel DORA delivery metrics ve birlikte okunmaları.
- High frequency + high fail rate yorumu.
- Lead-time value-stream decomposition.
- Team leaderboard riskleri.
- Goodhart's Law ve incentive design.
- Delivery + product outcome + SLO bağlantısı.

## Production/organizational failure modes
Takımları bağlamdan bağımsız rank etmek, deploy tanımını standardize etmemek, incident/hotfix verisini eksik toplamak, yalnızca velocity ölçmek ve metric değişiminden doğrudan nedensellik çıkarmak.

## Alıştırma / proje
Lead time 8 gün, haftada 1 deploy ve %5 fail-rate için üç diagnostic soru ve iki improvement experiment tasarla. `delivery-health-dashboard` ile leaderboard yerine trend, data-quality ve bottleneck hypothesis göster.

## Kaynaklar
- https://dora.dev/guides/dora-metrics/
- https://dora.dev/insights/dora-metrics-history/
- https://dora.dev/research/
