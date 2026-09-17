# Browser Release Cadence, Compatibility Risk & Progressive Delivery

## Konu anlatımı
Chrome 8 Eylül 2026'da Chrome 153 ile stable cadence'ini dört haftadan iki haftaya indirdi. Faster browser cadence frontend/platform ekipleri için daha sık compatibility events, daha kısa detection window ve daha güçlü automated validation ihtiyacı demektir.

Yeni web capability'leri version sniffing yerine mümkün olduğunca capability/feature detection ile kullanılmalı; fallback ve progressive rollout korunmalıdır. CI browser matrix synthetic journey'leri yakalarken RUM gerçek kullanıcı cihazı, network ve browser dağılımındaki etkiyi gösterir.

## Mental model
```text
browser release
      |
compatibility CI
      |
 capability/regression signal
   /             \
healthy          broken
   |               |
progressive     fallback /
rollout         flag off
   |
RUM + business KPI
```

## İçeride ne oluyor?
Browser update'i rendering, CSS, JavaScript veya Web API davranışını değiştirebilir. Platform ekibi release notes + automated matrix + capability probes ile değişiklikleri erken yakalar. Product rollout feature flag/cohort ile büyütülür; browser/version kırılımında telemetry tutulur.

## Mülakat soruları
- Faster release cadence riski nasıl değiştirir?
- Feature detection neden UA sniffing'den daha dayanıklıdır?
- Polyfill ile progressive enhancement farkı nedir?
- Browser matrix nasıl seçilir?
- RUM ve synthetic monitoring nasıl ayrılır?
- Senior: yeni Web API'yi nasıl canary edersin?
- Staff/EM: compatibility incident ownership'i nasıl tasarlanır?
- CTO: test maliyeti ile supported-browser revenue coverage nasıl dengelenir?

## Beklenen cevap seviyesi
Junior: compatibility/fallback. Mid: feature detection ve matrix. Senior: RUM, rollout ve rollback. Staff/EM: support policy ve ownership. Principal/CTO: revenue coverage, enterprise constraints ve platform economics.

## Mini alıştırma
Trafiğin %72'si Chromium, %18'i Safari, %8'i Firefox, %2'si diğer. Yalnız güncel Chromium'da bulunan bir API için launch planı, fallback ve abort metric'leri tasarla.

## Proje fikri
`browser-compat-gate`: Playwright browser matrix, capability probes, synthetic checkout journey ve feature-flag rollout gate. Browser/version bazında error ve conversion farkını raporla.

## Failure modes / trade-off / production
Sadece latest Chrome test etmek; UA sniffing'e aşırı güvenmek; fallback'i test etmemek; browser error rate'i business KPI'dan ayırmak; enterprise-managed eski sürümleri yok saymak. Production'da JS error rate, Core Web Vitals, capability coverage, task success ve browser-version dağılımı izlenmelidir.

## Kaynaklar
- https://developer.chrome.com/blog/chrome-two-week-start
- https://developer.chrome.com/release-notes/153
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Feature_detection
