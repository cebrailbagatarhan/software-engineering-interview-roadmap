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

## Mülakat soruları
- SLI, SLO, SLA ve error budget farkı nedir?
- Neden %100 reliability genellikle yanlış hedeftir?
- Burn rate neden actionable'dır?
- Freeze sırasında hangi değişikliklere izin verilir?
- Low-traffic SLO alerting neden zordur?
- Staff: dependency-caused outage attribution nasıl yapılır?
- CTO: product ve SRE incentive'ları nasıl hizalanır?

## Beklenen cevap seviyesi
Junior: SLI/SLO. Mid: budget hesabı. Senior: burn-rate ve incident attribution. Staff: cross-team policy. Principal/CTO: risk appetite, governance ve product economics.

## Mini alıştırma
Ayda 10 milyon eligible request ve %99.95 success SLO için budget'ı hesapla; 1,500 failure'lık incident'ın budget payını bul ve policy aksiyonu öner.

## Proje fikri
Traffic, SLO ve incident girdilerinden budget/burn-rate hesaplayıp canary/freeze kararlarını simüle eden dashboard yap.

## Failure modes / production
Kolay ölçülen ama kullanıcıyı temsil etmeyen SLI; %100 hedef; punishment culture; belirsiz ownership; dependency attribution kavgası; noisy low-traffic alerts. Remaining budget, multi-window burn rate, incident budget share, change failure ve reliability-work allocation izlenir.

## Kaynaklar
- Implementing SLOs: https://sre.google/workbook/implementing-slos/
- Error Budget Policy: https://sre.google/workbook/error-budget-policy/
- Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/
- Embracing Risk: https://sre.google/sre-book/embracing-risk/
