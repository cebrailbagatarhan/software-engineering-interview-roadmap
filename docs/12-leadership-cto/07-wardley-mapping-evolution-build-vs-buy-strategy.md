# Wardley Mapping, Evolution & Build-vs-Buy Strategy

**Seviye:** Senior → CTO  
**Alan:** Leadership / Product / Business / Architecture Strategy

## Konu anlatımı
Architecture seçimi yalnız teknoloji karşılaştırması değildir. Wardley Mapping bir capability'nin kullanıcı ihtiyacına/value chain'e göre görünürlüğünü ve genesis → custom-built → product/rental → commodity/utility evrimini aynı resimde tartışmaya yarayan stratejik araçtır.

Harita bir tahmin makinesi değildir. Ama “commodity queue'yu neden custom yazıyoruz?”, “differentiating algorithm outsource edilmeli mi?” veya “vendor lock-in hangi dependency'de stratejik risk?” gibi soruları dependency graph üzerinde görünür hale getirir. Build-vs-buy kararı lisans fiyatından daha geniştir: opportunity cost, switching cost, operational burden, strategic differentiation, data gravity, compliance ve market evolution birlikte değerlendirilir.

## Mental model
```text
Visibility / user need
^
| Customer need
|      |
| Differentiating workflow ---- proprietary capability
|      |                          |
|      +------ managed DB -------+---- object storage
|                  |
|               compute
+--------------------------------------------------> evolution
  Genesis      Custom-built       Product      Commodity/Utility
```

## İnvariant
Her şeyi custom yapmak stratejik kontrol değildir; her şeyi SaaS almak da otomatik hız değildir. Kontrol noktası differentiating capability, dependency risk ve reversibility kesişimidir.

## İçeride ne oluyor?
1. Harita teknoloji listesinden değil kullanıcı/consumer ihtiyacından başlar.
2. İhtiyacı sağlayan capabilities dependency/value chain olarak açılır.
3. Her capability'nin evolution aşaması hipotez olarak yerleştirilir.
4. Commodity'ye yaklaşan parçalar standardization, automation ve utility consumption'a adaydır.
5. Genesis/custom-built parçalar daha yüksek belirsizlik taşır; discovery/learning ağırlıklı yönetilir.
6. Build-vs-buy için TCO yanında time-to-market, reversibility, switching cost, data gravity, compliance ve talent scarcity değerlendirilir.
7. Market evrildikçe harita değişir; dün differentiator olan capability yarın commodity olabilir.

## Mülakat soruları
1. Build-vs-buy kararında lisans fiyatı dışında hangi maliyetler vardır?
2. Commodity capability'yi custom build etmek ne zaman mantıklıdır?
3. Vendor lock-in her zaman kötü müdür?
4. Auth sistemi için build/buy kararını nasıl çerçevelersin?
5. Platform ekibinin standardize edeceği capability'leri nasıl seçersin?
6. Differentiator commodity olursa architecture strategy nasıl değişir?
7. CTO seviyesinde roadmap, gross margin ve headcount bu karara nasıl bağlanır?

## Beklenen cevap seviyesi
- **Senior:** TCO, opportunity cost, operational ownership ve reversibility'yi tartışır.
- **Staff:** capability dependency ve cross-team platform etkisini görünür kılar.
- **Principal:** market evolution, ecosystem ve switching cost'u architecture portfolio'ya bağlar.
- **CTO:** differentiation, time-to-market, margin, compliance, capital allocation ve organizational capability'yi birlikte yönetir.

## Kısa alıştırma
B2B analytics SaaS için identity, billing, columnar storage, dashboard renderer, proprietary anomaly detector ve email delivery capability'lerini haritala. Her biri için build/buy/partner varsayımı ve kararı değiştirecek bir market sinyali yaz.

## Proje fikri
`strategy-map-casebook`: hayali SaaS'ın 12 capability'sini dependency graph + evolution ekseninde haritala. Auth-buy, anomaly-engine-build ve observability-managed-service için üç ADR üret; 3 yıllık TCO, switching planı ve kill criterion ekle.

## Failure modes / trade-off / production
Evolution konumunu objektif gerçek sanmak sahte kesinlik yaratır. Bugünkü vendor fiyatına aşırı odaklanmak migration, egress ve organizational switching cost'u gizler. “Core değilse outsource” kuralı security/compliance/latency constraints'i kaçırabilir. Kararlar reliability SLO, unit cost, vendor incidents, contract renewal, engineer toil, change lead time ve exit-test sonuçlarıyla periyodik yeniden değerlendirilmelidir.

## Kaynaklar
- Simon Wardley — Wardley Maps ebook repository: https://github.com/HiredThought/wardley-maps-ebook
- Simon Wardley — On Being Lost: https://medium.com/wardleymaps/on-being-lost-2ef5f05eb1ec
- FinOps Foundation — FinOps Framework: https://www.finops.org/framework/
