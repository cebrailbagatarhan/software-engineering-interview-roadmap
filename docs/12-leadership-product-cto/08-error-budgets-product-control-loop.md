# Error Budgets as a Product-Control Loop

## Konu anlatımı
SLO yalnız dashboard hedefi değildir. Error budget, reliability ile feature velocity arasındaki çatışmayı ölçülebilir karar mekanizmasına çevirir. %99.9 SLO, %0.1 failure budget demektir. Bütçe sağlıklıyken kontrollü risk alınabilir; hızlı burn veya exhaustion ise önceden tanımlanmış reliability aksiyonlarını tetikler.

## Mental model
```text
user expectation -> SLI -> SLO -> error budget
                                  /          \
                             healthy        burning
                                |              |
                            velocity       guardrails
                                               |
                                       reliability work
```

## İçeride ne oluyor?
SLI user-visible outcome'a yakın olmalıdır. Remaining budget toplam risk alanını, burn rate ise bu alanın tüketim hızını gösterir. Policy punishment değil control loop'tur. Google'ın örnek error-budget policy'si dört haftalık budget aşıldığında P0/security dışı değişiklikleri durdurmayı ve tek incident budget'ın %20'sinden fazlasını tüketirse postmortem'i örnekler; threshold'lar organizasyona göre kalibre edilmelidir.

Canary release bu kontrol döngüsünün actuator'larından biridir: candidate sürümü küçük trafik yüzdesine açmak, defect'in toplam budget etkisini exposure ile sınırlar. Bu nedenle release policy yalnız `deploy/no-deploy` değil; canary yüzdesi, observation window, rollback süresi ve kabul edilen budget spend birlikte tasarlanmalıdır.

## Mülakat soruları
- SLI, SLO, SLA ve error budget farkı nedir?
- Neden %100 reliability genellikle yanlış hedeftir?
- Burn rate neden actionable'dır?
- Freeze sırasında hangi değişikliklere izin verilir?
- Low-traffic SLO alerting neden zordur?
- Staff: dependency-caused outage attribution nasıl yapılır?
- CTO: product ve SRE incentive'ları nasıl hizalanır?
- Canary exposure ile error-budget riski arasındaki ilişki nedir?

## Beklenen cevap seviyesi
Junior: SLI/SLO. Mid: budget hesabı. Senior: burn-rate ve incident attribution. Staff: cross-team policy ve rollout guardrails. Principal/CTO: risk appetite, governance, product economics ve reliability investment allocation.

## Mini alıştırma
Ayda 20 milyon eligible request ve %99.95 success SLO için budget'ı hesapla; 4.000 failure'lık incident'ın budget payını bul. Ardından %5 canary ile aynı defect'in gözlem penceresindeki beklenen blast radius'unu tartış.

## Proje fikri
Traffic, SLO, incident ve canary-exposure girdilerinden budget/burn-rate hesaplayıp rollout/freeze kararlarını simüle eden dashboard yap. Deploy annotation'larını incident ve budget spend ile ilişkilendir.

## Failure modes / production
Kolay ölçülen ama kullanıcıyı temsil etmeyen SLI; %100 hedef; punishment culture; belirsiz ownership; dependency attribution kavgası; noisy low-traffic alerts; budget bitene kadar yalnız remaining-budget yüzdesine bakmak. Remaining budget, multi-window burn rate, incident budget share, canary exposure, rollback time, change failure ve reliability-work allocation izlenir.

## Kaynaklar
- Implementing SLOs: https://sre.google/workbook/implementing-slos/
- Error Budget Policy: https://sre.google/workbook/error-budget-policy/
- Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/
- Canarying Releases: https://sre.google/workbook/canarying-releases/
- Embracing Risk: https://sre.google/sre-book/embracing-risk/
