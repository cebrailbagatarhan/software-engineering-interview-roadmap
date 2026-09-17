# Self-hosted CI Runner Version Enforcement, Fleet Hygiene & Brownouts

## Konu anlatımı
Self-hosted CI runner, SaaS control plane ile uyumlu kalması gereken bir execution-plane ajanıdır. Version drift security kadar capacity ve delivery-reliability problemidir. GitHub Enterprise Cloud için minimum self-hosted runner version enforcement 25 Eylül 2026'da tam olarak devreye girecek; update'lerden 30 günden fazla geri kalan runner'lar job alamayabilir ve kritik security update durumunda job queueing update'e kadar durabilir.

```text
control plane -> min-version policy -> scheduler
                                  /          \
                            healthy pool   stale pool X
                                 |             |
                              jobs          queue growth
```

## Tasarım ilkeleri
Immutable runner image, merkezi version inventory, staged canary/waves, capacity headroom ve rollback runbook birlikte ele alınmalıdır. Brownout geçici hata değil, yaklaşan enforcement altında gerçek failure mode'un kontrollü provasıdır.

## Mülakat soruları
- Runner drift neden yalnız patch-management değildir?
- Brownout hangi varsayımları test eder?
- Immutable image neden pet runner'dan daha güvenlidir?
- Staff seviyesinde 5.000 runner'lık fleet rollout nasıl tasarlanır?
- CTO seviyesinde enforcement deadline ile feature delivery nasıl dengelenir?

## Production bağlantısı
Runner version coverage, registration failure, queue depth, pickup latency, job success, utilization ve replacement time izlenir. Fleet-wide tek dalga rollout ve eksik spare capacity temel blast-radius riskleridir.

## Kaynaklar
- https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/
- https://docs.github.com/actions/hosting-your-own-runners/managing-self-hosted-runners
