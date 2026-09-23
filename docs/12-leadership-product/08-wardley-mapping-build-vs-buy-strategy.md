# Wardley Mapping, Evolution & Build-vs-Buy Strategy

## Konu anlatımı
Architecture kararı yalnız “hangi teknoloji daha iyi?” sorusu değildir. Wardley Mapping, bir capability'nin kullanıcı ihtiyacına görünürlüğünü ve **genesis → custom-built → product/rental → commodity/utility** evrimini aynı haritada düşünmeyi sağlar. Amaç kesin tahmin değil; dependency, differentiation ve market maturity varsayımlarını görünür hale getirmektir.

Build-vs-buy kararı lisans fiyatından büyüktür: time-to-market, opportunity cost, switching cost, operational burden, data gravity, compliance, talent scarcity ve strategic differentiation birlikte değerlendirilmelidir.

```text
Visibility / user need
^
| Customer need
|      |
| Differentiating workflow ---- proprietary capability
|      |                         |
|      +------ managed DB ------+---- object storage
|                   |
|                compute
+------------------------------------------------> evolution
  Genesis       Custom-built       Product       Commodity/Utility
```

## İçeride ne oluyor?
1. Teknoloji listesinden değil kullanıcı/consumer ihtiyacından başlanır.
2. İhtiyacı sağlayan capabilities dependency/value chain olarak açılır.
3. Her capability mevcut evolution aşamasına yaklaşık yerleştirilir.
4. Commodity'ye yaklaşan parçalar standardization, automation ve utility consumption'a adaydır.
5. Genesis/custom-built parçalar daha fazla belirsizlik ve discovery ihtiyacı taşır.
6. Build-vs-buy değerlendirmesi TCO yanında reversibility, switching cost, compliance ve strategic control içerir.
7. Market evrildikçe harita ve architecture strategy yeniden değerlendirilir.

## Mülakat soruları
- Build-vs-buy kararında lisans fiyatı dışında ne hesaba katılır?
- Commodity capability'yi custom build etmek ne zaman mantıklıdır?
- Vendor lock-in her zaman kötü müdür?
- **Senior:** auth sistemi için build/buy kararını nasıl çerçevelersin?
- **Staff:** platform ekibinin standardize edeceği capabilities nasıl seçilir?
- **Principal:** differentiator commodity olursa architecture strategy nasıl değişir?
- **CTO:** roadmap, gross margin ve engineering headcount teknik kararı nasıl değiştirir?

## Beklenen cevap seviyesi
- **Senior:** TCO, opportunity cost, operational ownership ve reversibility'yi konuşur.
- **Staff:** dependency ve cross-team platform etkisini görünür kılar.
- **Principal:** evolution, ecosystem ve switching cost'u architecture portfolio'ya bağlar.
- **CTO:** teknik seçimleri differentiation, margin, compliance, capital allocation ve organizational capability ile birlikte yönetir.

## Mini alıştırma
B2B analytics SaaS için identity, billing, columnar storage, dashboard renderer, proprietary anomaly detector ve email delivery capability'lerini haritala. Her biri için build/buy/partner varsayımı ve kararı değiştirecek bir market sinyali yaz.

## Proje fikri
`strategy-map-casebook`: hayali SaaS'ın 12 capability'sini dependency + evolution haritasında göster. Auth buy, anomaly engine build ve observability managed-service için üç ADR üret; 3 yıllık TCO, switching planı ve kill criterion ekle.

## Failure modes / trade-off / production
Haritayı objektif gerçek sanmak sahte kesinlik yaratır. Bugünkü vendor fiyatına odaklanmak migration/data-egress ve organizational switching cost'u gizler. “Core değilse outsource” kuralı security/compliance/latency constraints'i kaçırabilir. Kararlar reliability SLO, unit cost, vendor incidents, contract renewal, engineer toil, lead time ve exit-test sonuçlarıyla periyodik yeniden değerlendirilmelidir.

## Kaynaklar
- Simon Wardley — Wardley Maps ebook repository: https://github.com/HiredThought/wardley-maps-ebook
- Simon Wardley — On Being Lost: https://medium.com/wardleymaps/on-being-lost-2ef5f05eb1ec
- FinOps Foundation — Framework: https://www.finops.org/framework/
