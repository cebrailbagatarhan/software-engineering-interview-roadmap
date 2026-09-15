# Error Budgets as Product & Reliability Governance

## Konu anlatımı
SLI kullanıcı açısından önemli bir service-level ölçümüdür; SLO bu ölçüm için hedefi, error budget ise hedefin izin verdiği başarısızlık payını karar mekanizmasına dönüştürür. Budget yalnız downtime dakikası değildir: good/bad event tanımı, ölçüm penceresi ve burn rate policy'nin davranışını belirler.

Leadership açısından error budget product velocity ile reliability investment arasında önceden tanımlanmış ortak dil sağlar. Budget sağlıklıyken kontrollü risk alınabilir; hızlı tüketimde release policy sıkılaştırılabilir ve reliability work öne çekilebilir. Ama budget bireysel performans metriğine çevrilirse Goodhart etkisi ve ölçüm manipülasyonu doğurabilir.

## Mental model
```text
user journey -> SLI -> SLO
                      |
                 error budget
                /           \
          healthy         fast burn
             |               |
       ship/experiment   reliability focus
```

## Mülakat soruları
- SLA/SLO/SLI farkı nedir?
- Error budget neden sadece downtime değildir?
- Burn rate neyi anlatır?
- Velocity/reliability çatışması nasıl yönetilir?
- Goodhart riski nedir?
- Feature freeze hangi koşullarda uygulanmalıdır?

## Seviye beklentisi
**Senior:** doğru SLI/SLO ve budget. **Staff/EM:** release policy, incident review ve reliability backlog. **CTO:** customer tier, revenue/risk, compliance ve organizational incentives.

## Mini alıştırma
Checkout için availability ve latency SLI seç; 30 günlük SLO ve budget exhaustion sonrası üç aşamalı policy yaz.

## Proje fikri
Rolling-window error-budget dashboard ve multi-window burn-rate alerting kur; deploy annotation'larıyla ilişkilendir.

## Production / failure modes
%100 SLO, kullanıcı yolculuğu yerine kolay infra metriği seçmek, budget'ı performans cezasına çevirmek, tüm müşteri tier'larına aynı hedefi uygulamak ve yalnız remaining-budget yüzdesine bakmak temel anti-pattern'lerdir.

## Kaynaklar
- https://sre.google/workbook/implementing-slos/
- https://sre.google/workbook/error-budget-policy/
- https://sre.google/workbook/alerting-on-slos/
